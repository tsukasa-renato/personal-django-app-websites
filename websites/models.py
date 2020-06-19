from django.db import models
from datetime import datetime
from utils import utils


# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField.upload_to
def icon_path(instance, filename):
    if len(filename) > 10:
        filename = filename[-10:]
    return f'{instance.url}/icon/{filename}'


class Websites(models.Model):
    url = models.CharField(max_length=50, unique=True, null=False, blank=False)
    images = models.ImageField(upload_to=icon_path, null=True, blank=True)
    title = models.CharField(max_length=20, null=False, blank=False)
    telephone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    youtube = models.CharField(max_length=50, null=True, blank=True)
    whatsapp = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    reason = models.CharField(max_length=100, null=True, blank=True)
    local_timezone = models.CharField(max_length=50, null=False, blank=False, default='America/Sao_Paulo')
    created_at = models.DateTimeField(default=datetime.now())
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
