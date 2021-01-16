from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('<slug:url>/', views.ShowProducts.as_view(), name='home'),
    path('<slug:url>/c/<slug:selected_category>/', views.ShowProducts.as_view(), name='category'),
    path('<slug:url>/p/<slug:selected_product>/', views.ShowProduct.as_view(), name='product'),
    path('<slug:url>/cart', views.Cart.as_view(), name='cart')
]
