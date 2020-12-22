from django.db import models
from websites.utils import utils, choices
from django.utils.text import slugify
from django.core.exceptions import ValidationError

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
        return utils.custom_datetime(self.created_at, self.websites.timezone)
    get_created_at.short_description = 'Created at'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self):
        """
        Formats the updated_at in the time zone registered on the website
        """
        return utils.custom_datetime(self.updated_at, self.websites.timezone)
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
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    promotional_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def get_price(self):
        """
        Formats the price in the currency informed in website
        """
        if self.price is not None:
            return utils.money_format(self.price, self.websites.currency, self.websites.language)
        return ''
    get_price.short_description = 'Price'
    get_price.admin_order_field = 'price'

    def get_promotional_price(self):
        """
        Formats the promotional price in the currency informed in website
        """
        if self.promotional_price is not None:
            return utils.money_format(self.promotional_price, self.websites.currency, self.websites.language)
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

    def check_promotional_price(self):

        if self.promotional_price is not None:

            if self.price is None:
                raise ValidationError("Price can't be None when the promotional_price is set")

            if self.price < self.promotional_price:
                raise ValidationError("Promotional price can't be less than price")

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
        if self.minimum > self.maximum:
            raise ValidationError("Minimum can't be less than the maximum")

    class Meta:
        abstract = True


class Enable(models.Model):
    is_available = models.BooleanField("Is available?", default=True)
    reason = models.CharField("Reason (optional, only for unavailable)", max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class PriceType(models.Model):
    price_type = models.CharField(
        "How is the price calculated?",
        max_length=1,
        default='1',
        choices=(
            ('1', "Only use the product price"),
            ('2', "Add the product price to the sum groups price"),
            ('3', "Add the product price to the average groups price"),
            ('4', "Sum all the groups price"),
            ('5', "Average all the groups price"),
        )
    )

    def check_price(self):
        if self.price_type not in ['4', '5', None] and self.get_real_price() is None:
            raise ValidationError("Enter a price or change the type price")
        if self.price_type not in ['1', '2', '3'] and self.get_real_price() is not None:
            raise ValidationError("Remove the price or change the type price")

    class Meta:
        abstract = True


class Websites(CreateUpdate, Enable):

    url = models.SlugField(max_length=30, unique=True, null=False, blank=False)
    title = models.CharField(max_length=20, null=False, blank=False)
    home = models.CharField("Homepage title", max_length=20, null=False, blank=False, default='Highlight')

    timezone = models.CharField(
        max_length=30,
        default='UTC',
        choices=choices.choice_timezones()
    )

    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=choices.choice_currencies()
    )

    language = models.CharField(
        max_length=11,
        default='en_US',
        choices=choices.choice_language()
    )

    def get_created_at(self):
        """
        Formats the created_at in the time zone registered on the website
        """
        return utils.custom_datetime(self.created_at, self.timezone)
    get_created_at.short_description = 'Created at'
    get_created_at.admin_order_field = 'created_at'

    def get_updated_at(self):
        """
        Formats the updated_at in the time zone registered on the website
        """
        return utils.custom_datetime(self.updated_at, self.timezone)
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

    navbar = models.CharField(max_length=6, null=True, blank=True)
    category = models.CharField(max_length=6, null=True, blank=True)
    active = models.CharField(max_length=6, null=True, blank=True)
    footer = models.CharField(max_length=6, null=True, blank=True)
    text = models.CharField(max_length=6, null=True, blank=True)
    title = models.CharField(max_length=6, null=True, blank=True)
    title_hover = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return 'colors'


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

        super().save(*args, **kwargs)


class Products(CreateUpdate, Enable, CommonInfo, Prices, PriceType):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    show_on_home = models.BooleanField("Show on homepage?", default=True)
    position = models.PositiveSmallIntegerField(default=1)

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

        self.check_promotional_price()

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Groups(CreateUpdate, Prices, MinMax, PriceType):

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
            ('1', "Only use the group price"),
            ('2', "Add the group price to the sum options price"),
            ('3', "Add the group price to the average options price"),
            ('4', "Sum all the options price"),
            ('5', "Average all the options price"),
        )
    )

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(fields=['products', 'slug'], name='unique_group')
        ]

    def __str__(self):
        return self.slug

    def check_price(self):
        if self.products.price_type == '1':
            if self.price_type is not None:
                raise ValidationError("Only the product price will be used, so group can't be priced")
        else:
            if self.price_type is None:
                raise ValidationError("Products require the group price, so price type can't be None")

        super().check_price()

    def save(self, *args, **kwargs):

        self.check_promotional_price()

        self.check_price()

        self.check_min_max()

        self.slug = f'{slugify(self.title)}'

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

    def check_max_max(self):
        if self.maximum > self.groups.maximum:
            raise ValidationError("Options' maximum can't be greater than Groups' maximum")

    def check_price(self):
        if self.get_real_price():
            if self.groups.price_type == '1':
                raise ValidationError("Only the group price will be used")
            if self.groups.price_type is None:
                raise ValidationError("Only the product price will be used")

    def save(self, *args, **kwargs):

        self.check_promotional_price()

        self.check_price()

        self.check_min_max()

        self.check_max_max()

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)
