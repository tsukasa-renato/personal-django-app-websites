from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('<url>/', views.ShowProducts.as_view(), name='home'),
    path('<url>/c/<selected_category>/', views.ShowProducts.as_view(), name='category'),
    path('<url>/p/<selected_product>/', views.ShowProduct.as_view(), name='product'),
    path('<url>/cart', views.Cart.as_view(), name='cart')
]
