from django.db import models
from utils import utils
from django.utils.text import slugify


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
            raise ValueError("Minimum can't be less than the maximum")

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
        default=1,
        choices=(
            ('1', "Only use the product price"),
            ('2', "Add the product price to the sum groups price"),
            ('3', "Add the product price to the average groups price"),
            ('4', "Sum all the groups price"),
            ('5', "Average all the groups price"),
        )
    )

    def check_price(self):
        if self.price_type in ['1', '2', '3'] and self.price is None:
            raise ValueError("Enter a price or change the type price")
        if self.price_type in ['4', '5'] and self.price is not None:
            raise ValueError("Remove the price or change the type price")

    class Meta:
        abstract = True


class Websites(CreateUpdate, Enable):

    url = models.SlugField(max_length=30, unique=True, null=False, blank=False)
    title = models.CharField(max_length=20, null=False, blank=False)
    home = models.CharField("Homepage title", max_length=20, null=False, blank=False, default='Highlight')

    timezone = models.CharField(max_length=50, null=False, blank=False, default='auto')
    currency = models.CharField(max_length=10, null=False, blank=False, default='auto')

    def get_created_at(self):
        if self.timezone == 'auto':
            return utils.custom_datetime(self.created_at)

        return utils.custom_datetime(self.created_at, self.timezone)
    get_created_at.short_description = 'Created at'

    def get_updated_at(self):
        if self.timezone == 'auto':
            return utils.custom_datetime(self.updated_at)

        return utils.custom_datetime(self.updated_at, self.timezone)
    get_updated_at.short_description = 'Updated at'

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'

    def __str__(self):
        return self.url


class Contacts(CreateUpdate):

    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)

    telephone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    facebook = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    pinterest = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    linkedin = models.CharField(max_length=50, null=True, blank=True)
    youtube = models.CharField(max_length=100, null=True, blank=True)
    twitch = models.CharField(max_length=100, null=True, blank=True)
    discord = models.CharField(max_length=200, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.websites


class Colors(CreateUpdate):

    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)

    navbar = models.CharField(max_length=6, null=False, blank=False, default='0080FF')
    categories = models.CharField(max_length=6, null=False, blank=False, default='F03333')
    active = models.CharField(max_length=6, null=False, blank=False, default='E62D2D')
    footer = models.CharField(max_length=6, null=False, blank=False, default='F03333')
    text = models.CharField(max_length=6, null=False, blank=False, default='FFFFFF')
    title = models.CharField(max_length=6, null=False, blank=False, default='000000')
    title_hover = models.CharField(max_length=6, null=False, blank=False, default='F03333')

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.websites


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
        return self.websites


class Banners(CreateUpdate):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)

    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=False, blank=False)
    link = models.SlugField(max_length=30, null=True, blank=True)

    position = models.PositiveIntegerField(default=1)

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
    position = models.PositiveIntegerField(default=1)

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
    show_home = models.BooleanField("Show in homepage?", default=True)
    position = models.PositiveIntegerField(default=1)

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

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Groups(CreateUpdate, Prices, MinMax, PriceType):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)

    title = models.CharField(max_length=50, null=False, blank=False)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(fields=['products', 'slug'], name='unique_group')
        ]

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):

        self.check_price()

        self.check_min_max()

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Options(CreateUpdate, CommonInfo, Prices, MinMax):

    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=200, null=False, blank=True)
    position = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Option',
        verbose_name_plural = 'Options'
        constraints = [
            models.UniqueConstraint(fields=['groups', 'slug'], name='unique_options')
        ]

    def __str__(self):
        return self.slug

    def check_max_max(self):
        if self.maximum > self.groups__maximum:
            raise ValueError("Options' maximum can't be greater than Groups' maximum")

    def save(self, *args, **kwargs):

        self.check_min_max()

        self.check_max_max()

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)
