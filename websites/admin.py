from django.contrib import admin
from . import models


class WebsitesAdmin(admin.ModelAdmin):
    list_display = ['url', 'get_created_at', 'get_updated_at']


admin.site.register(models.Websites, WebsitesAdmin)
