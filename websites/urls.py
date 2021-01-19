from django.urls import path, include
from . import views

app_name = 'websites'

urlpatterns = [
    path('<slug:url>/', include([
        path('', views.ShowProducts.as_view(), name='home'),
        path('c/<slug:selected_category>/', views.ShowProducts.as_view(), name='category'),
        path('p/<slug:selected_product>/', views.ShowProduct.as_view(), name='product'),
        path('cart', views.Cart.as_view(), name='cart')
    ]))
]
