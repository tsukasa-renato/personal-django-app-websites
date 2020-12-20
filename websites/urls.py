from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('<url>/', views.ShowProducts.as_view(), name='home'),
    path('<url>/<selected_category>/', views.ShowProducts.as_view(), name='category'),
    path('<url>/p/<selected_product>/', views.ShowProduct.as_view(), name='product'),
    path('<url>/p/<product>/addedtocart', views.ShowProduct.as_view(), name='addtocart')
]
