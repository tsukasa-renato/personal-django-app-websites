from django.contrib import admin
from . import models


class ColorsInline(admin.TabularInline):
    model = models.Colors


class IconsInline(admin.TabularInline):
    model = models.Icons


class WebsitesAdmin(admin.ModelAdmin):
    list_display = ['url', 'get_created_at', 'get_updated_at']
    inlines = [
        ColorsInline,
        IconsInline
    ]


class OptionsInline(admin.TabularInline):
    model = models.Options


class GroupsAdmin(admin.ModelAdmin):
    list_display = ['title', 'calculation', 'minimum', 'maximum']
    inlines = [
        OptionsInline
    ]


class ProductsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'images']


admin.site.register(models.Websites, WebsitesAdmin)
admin.site.register(models.Categories)
admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Groups, GroupsAdmin)
admin.site.register(models.Options)
admin.site.register(models.Banners)
admin.site.register(models.Contacts)
admin.site.register(models.Icons)
admin.site.register(models.Colors)
