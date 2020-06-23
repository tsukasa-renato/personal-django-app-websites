from django.db import models
from utils import utils


# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField.upload_to
def icon_path(instance, filename):
    if len(filename) > 10:
        filename = filename[-10:]
    return f'{instance.url}/icon/{filename}'


def image_path(instance, filename):
    if len(filename) > 50:
        filename = filename[-50:]
    return f'{instance.websites.url}/images/{filename}'


class Websites(models.Model):
    url = models.SlugField(max_length=30, unique=True, null=False, blank=False)
    images = models.ImageField(upload_to=icon_path, null=True, blank=True)
    title = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=20, null=False, blank=False, default='red')
    telephone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, null=True, blank=True)
    local_timezone = models.CharField(max_length=50, null=False, blank=False, default='America/Sao_Paulo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    def get_created_at(self):
        if self.local_timezone == 'auto':
            return utils.custom_datetime(self.created_at)

        return utils.custom_datetime(self.created_at, self.local_timezone)
    get_created_at.short_description = 'Created at'

    def get_updated_at(self):
        if self.local_timezone == 'auto':
            return utils.custom_datetime(self.updated_at)

        return utils.custom_datetime(self.updated_at, self.local_timezone)
    get_updated_at.short_description = 'Updated at'

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'


class Categories(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False, blank=False)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    position = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'title'], name='unique_category'),
        ]

    def __str__(self):
        return self.title


class Products(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)
    calculation = models.CharField(
        default='1',
        max_length=1,
        choices=(
            ('1', 'Unique Price'),
            ('2', 'Total Sum')
        )
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    promotional_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    position = models.PositiveIntegerField(null=False, blank=False)
    stock = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_highlight = models.BooleanField(default=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'title'], name='unique_product')
        ]

    def __str__(self):
        return self.title


class Groups(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    calculation = models.CharField(
        default='1',
        max_length=1,
        choices=(
            ('1', 'Sum'),
            ('2', 'Average')
        )
    )
    minimum = models.PositiveIntegerField(default=1)
    maximum = models.PositiveIntegerField(default=1)
    can_repeat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'products', 'title'], name='unique_group')
        ]

    def __str__(self):
        return self.title


class Options(models.Model):
    websites = models.ForeignKey(Websites, on_delete=models.CASCADE)
    groups = models.ForeignKey(Groups, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    images = models.ImageField(upload_to=image_path, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    promotional_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    minimum = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Option',
        verbose_name_plural = 'Options'
        constraints = [
            models.UniqueConstraint(fields=['websites', 'groups', 'title'], name='unique_options')
        ]

    def __str__(self):
        return self.title


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


class SocialMedia(models.Model):
    websites = models.OneToOneField(Websites, on_delete=models.CASCADE, primary_key=True)
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
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'

    def __str__(self):
        return 'Social Media'
