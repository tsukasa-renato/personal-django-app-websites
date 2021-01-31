from rest_framework import serializers
from websites.models import Websites, Colors, Icons, Contacts, Banners, Categories, \
    Products, Groups, Options


class WebsitesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Websites
        fields = ['pk', 'url', 'title', 'home', 'timezone', 'currency', 'language', 'is_available', 'created_at',
                  'updated_at']


class ColorsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())

    class Meta:
        model = Colors
        fields = ['websites', 'navbar', 'category', 'active', 'footer', 'text', 'title', 'title_hover', 'cart',
                  'subcart', 'created_at', 'updated_at']


class IconsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())

    class Meta:
        model = Icons
        fields = ['websites', 'shortcut', 'account', 'cart', 'search', 'home', 'created_at', 'updated_at']


class ContactsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())

    class Meta:
        model = Contacts
        fields = ['websites', 'telephone', 'email', 'facebook', 'instagram', 'twitter', 'linkedin', 'pinterest',
                  'youtube', 'whatsapp', 'social_media_text', 'whatsapp_text']


class BannersSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())

    class Meta:
        model = Banners
        fields = ['pk', 'websites', 'images', 'link', 'position', 'created_at', 'updated_at']


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())

    class Meta:
        model = Categories
        fields = ['pk', 'websites', 'title', 'icon', 'slug', 'position', 'created_at', 'updated_at']


class ProductsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())
    categories = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Categories.objects.all())

    class Meta:
        model = Products
        fields = ['pk', 'websites', 'categories', 'title', 'description', 'images', 'slug', 'price_type', 'price',
                  'promotional_price', 'position', 'show_on_home', 'is_available', 'reason', 'created_at',
                  'updated_at']


class GroupsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())
    products = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Products.objects.all())

    class Meta:
        model = Groups
        fields = ['pk', 'websites', 'products', 'title', 'slug', 'price_type', 'maximum', 'minimum', 'position',
                  'created_at', 'updated_at']


class OptionsSerializer(serializers.HyperlinkedModelSerializer):

    websites = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Websites.objects.all())
    groups = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Groups.objects.all())

    class Meta:
        model = Options
        fields = ['pk', 'websites', 'groups', 'title', 'description', 'images', 'slug', 'price', 'promotional_price',
                  'position', 'maximum', 'minimum', 'created_at', 'updated_at']