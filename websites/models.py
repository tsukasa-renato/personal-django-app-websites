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


class Websites(models.Model):
    url = models.SlugField(max_length=30, unique=True, null=False, blank=False)
    title = models.CharField(max_length=20, null=False, blank=False)
    home = models.CharField(max_length=20, null=False, blank=False, default='Highlight')
    is_active = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=50, null=False, blank=False, default='auto')
    currency = models.CharField(max_length=10, null=False, blank=False, default='auto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

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


class Contacts(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return 'Contacts'


class Colors(models.Model):
    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)
    navbar = models.CharField(max_length=6, null=False, blank=False, default='0080FF')
    categories = models.CharField(max_length=6, null=False, blank=False, default='F03333')
    active = models.CharField(max_length=6, null=False, blank=False, default='E62D2D')
    footer = models.CharField(max_length=6, null=False, blank=False, default='F03333')
    text = models.CharField(max_length=6, null=False, blank=False, default='FFFFFF')
    title = models.CharField(max_length=6, null=False, blank=False, default='000000')
    title_hover = models.CharField(max_length=6, null=False, blank=False, default='F03333')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return 'Colors'


class Icons(models.Model):
    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)
    shortcut = models.ImageField(upload_to=icon_path, null=True, blank=True)
    account = models.ImageField(upload_to=icon_path, null=True, blank=True)
    cart = models.ImageField(upload_to=icon_path, null=True, blank=True)
    search = models.ImageField(upload_to=icon_path, null=True, blank=True)
    home = models.ImageField(upload_to=icon_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Icon'
        verbose_name_plural = 'Icons'

    def __str__(self):
        return 'Icons'


class Banners(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=False, blank=False)
    link = models.SlugField(max_length=30, null=True, blank=True)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.images.url


class Categories(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False, blank=False)
    icon = models.ImageField(upload_to=icon_path, null=True, blank=True)
    slug = models.SlugField(max_length=20, null=False, blank=True)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'slug'], name='unique_category'),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Products(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=False, blank=True)
    price_type = models.CharField(
        default='1',
        max_length=1,
        choices=(
            ('1', 'Independent'),
            ('2', 'Partially Dependent'),
            ('3', 'Totally Dependent')
        )
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    promotional_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    position = models.PositiveIntegerField(default=1)
    show_home = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'slug'], name='unique_product')
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Groups(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    slug = models.SlugField(max_length=200, null=False, blank=True)
    user_input = models.CharField(
        default='1',
        max_length=1,
        choices=(
            ('1', 'default'),
            ('2', 'text'),
            ('3', 'number'),
            ('4', 'date'),
            ('5', 'color'),
            ('6', 'image')
        )
    )
    calculation = models.CharField(
        default='1',
        max_length=1,
        choices=(
            ('1', 'Sum'),
            ('2', 'Average')
        )
    )
    price_type = models.CharField(
        default='3',
        max_length=1,
        choices=(
            ('1', 'Independent'),
            ('2', 'Partially Dependent'),
            ('3', 'Totally Dependent')
        )
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    promotional_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    minimum = models.PositiveIntegerField(default=1)
    maximum = models.PositiveIntegerField(default=1)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(fields=['products', 'slug'], name='unique_group')
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)


class Options(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=False, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    promotional_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    minimum = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField(default=1)
    position = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Option',
        verbose_name_plural = 'Options'
        constraints = [
            models.UniqueConstraint(fields=['groups', 'slug'], name='unique_options')
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.slug = f'{slugify(self.title)}'

        super().save(*args, **kwargs)
