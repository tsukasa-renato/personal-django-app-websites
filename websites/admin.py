from django.contrib import admin
from . import models


class WebsitesAdmin(admin.ModelAdmin):
    list_display = ['url', 'get_created_at', 'get_updated_at']


class OptionsInline(admin.TabularInline):
    model = models.Options


class GroupsInline(admin.TabularInline):
    model = models.Groups


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'images']


admin.site.register(models.Websites, WebsitesAdmin)
admin.site.register(models.Categories)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Groups)
admin.site.register(models.Options)
admin.site.register(models.Banners)
