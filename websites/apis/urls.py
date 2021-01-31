from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'websites', WebsitesViewSet)
router.register(r'colors', ColorsViewSet)
router.register(r'icons', IconsViewSet)
router.register(r'contacts', ContactsViewSet)
router.register(r'banners', BannersViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'groups', GroupsViewSet)
router.register(r'options', OptionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
