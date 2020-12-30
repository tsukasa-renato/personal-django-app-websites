from django.contrib import admin
from .models import Websites, Categories, Products, Groups, Options, \
    Banners, Contacts, Icons, Colors


class ContactsInline(admin.StackedInline):
    model = Contacts


class IconsInline(admin.StackedInline):
    model = Icons


class ColorsInline(admin.StackedInline):
    model = Colors


class WebsitesAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'home', 'timezone', 'currency', 'language', 'is_available', 'get_created_at',
                    'get_updated_at')
    actions_selection_counter = False

    inlines = [
        ContactsInline,
        IconsInline,
        ColorsInline,
    ]


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'get_created_at', 'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'images', 'get_price', 'get_promotional_price', 'price_type',
                    'is_available', 'get_created_at', 'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_type', 'maximum', 'minimum', 'get_created_at', 'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class OptionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_price', 'get_promotional_price', 'maximum', 'minimum', 'get_created_at',
                    'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class BannersAdmin(admin.ModelAdmin):
    list_display = ('images', 'link', 'get_created_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('email', 'telephone', 'facebook', 'twitter', 'linkedin', 'instagram', 'get_created_at',
                    'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class IconsAdmin(admin.ModelAdmin):
    list_display = ('shortcut', 'account', 'cart', 'search', 'home', 'get_created_at', 'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


class ColorsAdmin(admin.ModelAdmin):
    list_display = ('navbar', 'category', 'active', 'footer', 'text', 'title', 'title_hover', 'get_created_at',
                    'get_updated_at')
    actions_selection_counter = False
    show_full_result_count = False
    list_select_related = ('websites',)


admin.site.register(Websites, WebsitesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(Options, OptionsAdmin)
admin.site.register(Banners, BannersAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Icons, IconsAdmin)
admin.site.register(Colors, ColorsAdmin)
