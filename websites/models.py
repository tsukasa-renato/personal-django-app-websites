from django.db import models
from .utils.utils import custom_datetime, money_format, hexadecimal
from .utils.choices import currencies, timezones, languages
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
import decimal

# TODO: Create validations for the websites model
# TODO: Create validations for the contacts model


# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField.upload_to
def icon_path(instance, filename):
    if len(filename) > 10:
        filename = filename[-10:]
    return f'{instance.websites.url}/icon/{filename}'


def image_path(instance, filename):
    if len(filename) > 50:
        filename = filename[-50:]
    return f'{instance.websites.url}/images/{filename}'


class CreateUpdate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_created_at(self):
        """
        Formats the created_at in the time zone registered on the website
        """
        return custom_datetime(self.created_at, self.websites.timezone)
    get_created_at.short_description = 'Created at'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self):
        """
        Formats the updated_at in the time zone registered on the website
        """
        return custom_datetime(self.updated_at, self.websites.timezone)
    get_updated_at.short_description = 'Updated at'
    get_updated_at.admin_order_field = 'updated_at'

    class Meta:
        abstract = True


class CommonInfo(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)

    class Meta:
        abstract = True


class Prices(models.Model):
    price = models.DecimalField("price, only numbers", max_digits=12, decimal_places=2, null=True, blank=True)
    promotional_price = models.DecimalField("promotional price, only numbers", max_digits=12, decimal_places=2,
                                            null=True, blank=True)

    def get_price(self):
        """
        Formats the price in the currency informed in website
        """
        if self.price is not None:
            return money_format(self.price, self.websites.currency, self.websites.language)
        return ''
    get_price.short_description = 'Price'
    get_price.admin_order_field = 'price'

    def get_promotional_price(self):
        """
        Formats the promotional price in the currency informed in website
        """
        if self.promotional_price is not None:
            return money_format(self.promotional_price, self.websites.currency, self.websites.language)
        return ''
    get_promotional_price.short_description = 'Promotional price'
    get_promotional_price.admin_order_field = 'promotional_price'

    def get_real_price(self):
        """
        The get_real_price method checks if the option is in the promotion and returns the promotional_price else it
        returns price else returns None.
        """
        if self.promotional_price is not None:
            return self.promotional_price

        if self.price is not None:
            return self.price

        return None

    def check_price(self):

        if self.price is not None:
            if type(self.price) not in [int, float, decimal.Decimal]:
                raise ValidationError("Price needs be positive integer or float - type received: " +
                                      str(type(self.price)))

            if self.price < 0:
                raise ValidationError("Price can't be negative")

        if self.promotional_price is not None:

            if type(self.promotional_price) not in [int, float]:
                raise ValidationError("Promotional price needs be positive integer or float - type received: " +
                                      str(type(self.promotional_price)))

            if self.promotional_price < 0:
                raise ValidationError("Promotional price can't be negative")

            if self.price is None:
                raise ValidationError("Price can't be None when the promotional_price is set")

            if self.price < self.promotional_price:
                raise ValidationError("Promotional price can't be greater than price")

    class Meta:
        abstract = True


class MinMax(models.Model):
    minimum = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField(default=1)

    def max(self):
        return self.maximum

    def min(self):
        return self.minimum

    def check_min_max(self):
        if type(self.minimum) is not int:
            raise ValidationError("Minimum needs be positive integer - type received: " +
                                  str(type(self.minimum)))

        if type(self.maximum) is not int:
            raise ValidationError("Maximum needs be positive integer - type received: " +
                                  str(type(self.maximum)))

        if self.minimum < 0:
            raise ValidationError("Minimum can't be negative")

        if self.maximum <= 0:
            raise ValidationError("Maximum can't be negative or zero")

        if self.minimum > self.maximum:
            raise ValidationError("Minimum can't be greater than the maximum")

    class Meta:
        abstract = True


class Enable(models.Model):
    is_available = models.BooleanField("Is available?", default=True)
    reason = models.CharField("Reason (optional, only for unavailable)", max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class Websites(CreateUpdate, Enable):

    url = models.SlugField(max_length=30, unique=True, null=False, blank=False)
    title = models.CharField(max_length=20, null=False, blank=False)
    home = models.CharField("Homepage title", max_length=20, null=False, blank=False, default='Highlight')

    timezone = models.CharField(
        max_length=30,
        default='UTC',
        choices=timezones()
    )

    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=currencies()
    )

    language = models.CharField(
        max_length=11,
        default='en_US',
        choices=languages()
    )

    def get_created_at(self):
        """
        Formats the created_at in the time zone registered on the website
        """
        return custom_datetime(self.created_at, self.timezone)
    get_created_at.short_description = 'Created at'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self):
        """
        Formats the updated_at in the time zone registered on the website
        """
        return custom_datetime(self.updated_at, self.timezone)
    get_updated_at.short_description = 'Updated at'
    get_updated_at.admin_order_field = 'updated_at'

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'

    def __str__(self):
        return self.url


class Contacts(CreateUpdate):

    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)

    telephone = models.CharField("Telephone, only numbers", max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)

    facebook = models.CharField("facebook.com/", max_length=50, null=True, blank=True)
    instagram = models.CharField("instagram.com/", max_length=50, null=True, blank=True)
    pinterest = models.CharField("pinterest.com/", max_length=50, null=True, blank=True)
    twitter = models.CharField("twitter.com/", max_length=50, null=True, blank=True)
    linkedin = models.CharField("linkedin.com/in/", max_length=50, null=True, blank=True)
    youtube = models.CharField("youtube.com/channel/", max_length=100, null=True, blank=True)

    whatsapp = models.CharField("Whatsapp, only numbers (e.g. DD999555566)", max_length=20, null=True, blank=True)

    social_media_text = models.CharField("Type a message (e.g. follow us)", max_length=50, null=True, blank=True)
    whatsapp_text = models.CharField("Type a message (e.g. my whatsapp is)", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return 'contacts'


class Colors(CreateUpdate):

    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)

    navbar = models.CharField("Navbar color (hexadecimal): ", max_length=6, null=True, blank=True)
    category = models.CharField("Categories bar color (hexadecimal):", max_length=6, null=True, blank=True)
    active = models.CharField("Active category color (hexadecimal): ", max_length=6, null=True, blank=True)
    footer = models.CharField("Footer color (hexadecimal): ", max_length=6, null=True, blank=True)
    text = models.CharField("Text color (hexadecimal): ", max_length=6, null=True, blank=True)
    title = models.CharField("Title color (hexadecimal): ", max_length=6, null=True, blank=True)
    title_hover = models.CharField("Mouse hover color (hexadecimal): ", max_length=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return 'colors'

    def save(self, *args, **kwargs):

        if self.navbar is not None:
            self.navbar = hexadecimal(self.navbar)
            if not self.navbar:
                raise ValidationError("Navbar error: invalid hexadecimal")

        if self.category is not None:
            self.category = hexadecimal(self.category)
            if not self.category:
                raise ValidationError("Category error: invalid hexadecimal")

        if self.active is not None:
            self.active = hexadecimal(self.active)
            if not self.active:
                raise ValidationError("Active error: invalid hexadecimal")

        if self.footer is not None:
            self.footer = hexadecimal(self.footer)
            if not self.footer:
                raise ValidationError("Footer error: invalid hexadecimal")

        if self.text is not None:
            self.text = hexadecimal(self.text)
            if not self.text:
                raise ValidationError("Text error: invalid hexadecimal")

        if self.title is not None:
            self.title = hexadecimal(self.title)
            if not self.title:
                raise ValidationError("Title error: invalid hexadecimal")

        if self.title_hover is not None:
            self.title_hover = hexadecimal(self.title_hover)
            if not self.title_hover:
                raise ValidationError("Title hover error: invalid hexadecimal")

        super().save(*args, **kwargs)


class Icons(CreateUpdate):

    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)

    shortcut = models.ImageField(upload_to=icon_path, null=True, blank=True)
    account = models.ImageField(upload_to=icon_path, null=True, blank=True)
    cart = models.ImageField(upload_to=icon_path, null=True, blank=True)
    search = models.ImageField(upload_to=icon_path, null=True, blank=True)
    home = models.ImageField(upload_to=icon_path, null=True, blank=True)

    class Meta:
        verbose_name = 'Icon'
        verbose_name_plural = 'Icons'

    def __str__(self):
        return 'icons'


class Banners(CreateUpdate):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    images = models.ImageField(upload_to=image_path, null=False, blank=False)
    link = models.SlugField(max_length=30, null=True, blank=True)

    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.images.url


class Categories(CreateUpdate):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)

    title = models.CharField(max_length=20, null=False, blank=False)
    icon = models.ImageField(upload_to=icon_path, null=True, blank=True)

    slug = models.SlugField(max_length=20, null=False, blank=True)
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'slug'], name='unique_category'),
        ]

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):

        self.slug = f'{slugify(self.title)}'

        if self.slug == '-':
            self.slug = f'category{self.pk}'

        super().save(*args, **kwargs)


class Products(CreateUpdate, Enable, CommonInfo, Prices):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    show_on_home = models.BooleanField("Show on homepage?", default=True)
    position = models.PositiveSmallIntegerField(default=1)

    price_type = models.CharField(
        "How is the price calculated?",
        max_length=1,
        default='1',
        choices=(
            ('1', "Only use the product price"),
            ('2', "Add the product price to the sum groups price"),
            ('3', "Sum all the groups price"),
        )
    )

    def check_price_type(self):
        if type(self.price_type) is not str:
            raise ValidationError("Price type needs be string - type received: " + str(type(self.price_type)))
        if self.price_type not in ['1', '2', '3']:
            raise ValidationError("Invalid value - type a valid value -> '1' '2' '3'")
        if self.price_type in ['1', '2'] and self.get_real_price() is None:
            raise ValidationError(f"Price type = {self.price_type} requires a price. Enter a price or change the type "
                                  f"price")
        if self.price_type in ['3'] and self.get_real_price() is not None:
            raise ValidationError(f"Price type = {self.price_type} don't requires a price. Remove the price or change "
                                  f"the type price")

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'slug'], name='unique_product')
        ]

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):

        self.check_price()

        self.check_price_type()

        self.slug = f'{slugify(self.title)}'

        if self.slug == '-':
            self.slug = f'product{self.pk}'

        super().save(*args, **kwargs)


class Groups(CreateUpdate, MinMax):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)

    title = models.CharField(max_length=50, null=False, blank=False)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    position = models.PositiveSmallIntegerField(default=1)

    price_type = models.CharField(
        "How is the price calculated?",
        max_length=1,
        null=True,
        blank=True,
        choices=(
            ('1', "Sum all the options price"),
            ('2', "Average all the options price"),
        )
    )

    def check_price_type(self):
        if type(self.price_type) is not str and self.price_type is not None:
            raise ValidationError("Price type needs be string or None - type received: " + str(type(self.price_type)))
        if self.price_type not in [None, '1', '2']:
            raise ValidationError("Invalid value - type a valid value -> None '1' '2'")
        if self.products.price_type in ['1'] and self.price_type in ['1', '2']:
            raise ValidationError("Only product price is used, set price type to None")
        if self.products.price_type not in ['1'] and self.price_type in [None]:
            raise ValidationError("Product requires the options price - price type can't be None")

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(fields=['products', 'slug'], name='unique_group')
        ]

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):

        self.check_price_type()

        self.check_min_max()

        self.slug = f'{slugify(self.title)}'

        if self.slug == '-':
            self.slug = f'group{self.pk}'

        super().save(*args, **kwargs)


class Options(CreateUpdate, CommonInfo, Prices, MinMax):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    position = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = 'Option',
        verbose_name_plural = 'Options'
        constraints = [
            models.UniqueConstraint(fields=['groups', 'slug'], name='unique_options')
        ]

    def __str__(self):
        return self.slug

    def check_min_max(self):
        super().check_min_max()
        if self.maximum > self.groups.maximum:
            raise ValidationError("Options' maximum can't be greater than Groups' maximum")

    def check_price_type(self):
        if self.get_real_price():
            if self.groups.price_type is None:
                raise ValidationError("Only the product price will be used")
        else:
            if self.groups.price_type is not None:
                raise ValidationError("Product requires price will be used")

    def check_input_type(self):

        if self.groups.maximum == 1 and self.groups.minimum == 1 and self.minimum == 0:
            return 'radio'

        if self.maximum == 1:
            return 'checkbox'

        return 'number'

    def save(self, *args, **kwargs):

        self.check_price()

        self.check_price_type()

        self.check_min_max()

        self.slug = f'{slugify(self.title)}'

        if self.slug == '-':
            self.slug = f'option{self.pk}'

        super().save(*args, **kwargs)
