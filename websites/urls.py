from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('<url>/', views.Home.as_view(), name='home'),
    path('<url>/<category>/', views.Home.as_view(), name='category'),
    path('<url>/p/<product>/', views.Product.as_view(), name='product'),
    path('<url>/p/<product>/addedtocart', views.Product.as_view(), name='addtocart')
]
