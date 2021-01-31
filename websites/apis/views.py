from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from websites.models import Websites, Colors, Icons, Contacts, Banners, Categories, \
    Products, Groups, Options


class WebsitesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow websites to be viewed or edited
    """

    queryset = Websites.objects.all().order_by('pk')
    serializer_class = WebsitesSerializer
    permission_classes = [permissions.IsAuthenticated]


class ColorsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow colors to be viewed or edited
    """

    queryset = Colors.objects.all().order_by('pk')
    serializer_class = ColorsSerializer
    permission_classes = [permissions.IsAuthenticated]


class IconsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow icons to be viewed or edited
    """

    queryset = Icons.objects.all().order_by('pk')
    serializer_class = IconsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow contacts to be viewed or edited
    """

    queryset = Contacts.objects.all().order_by('pk')
    serializer_class = ContactsSerializer
    permission_classes = [permissions.IsAuthenticated]


class BannersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow banners to be viewed or edited
    """

    queryset = Banners.objects.all().order_by('pk')
    serializer_class = BannersSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoriesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow websites to be viewed or edited
    """

    queryset = Categories.objects.all().order_by('pk')
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow products to be viewed or edited
    """

    queryset = Products.objects.all().order_by('position')
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow groups to be viewed or edited
    """

    queryset = Groups.objects.all().order_by('pk')
    serializer_class = GroupsSerializer
    permission_classes = [permissions.IsAuthenticated]


class OptionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allow options to be viewed or edited
    """

    queryset = Options.objects.all().order_by('pk')
    serializer_class = OptionsSerializer
    permission_classes = [permissions.IsAuthenticated]
