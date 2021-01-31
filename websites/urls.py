from django.urls import path, include
from . import views
from .apis import urls

app_name = 'websites'

urlpatterns = [
    path('api/', include(urls.urlpatterns)),
    path('<slug:url>/', include([

        path('', views.ShowProducts.as_view(), name='home'),
        path('c/<slug:selected_category>/', views.ShowProducts.as_view(), name='category'),

        path('p/<slug:selected_product>/', include([
            path('', views.ShowProduct.as_view(), name='product'),
            path('edit-<int:position>/', views.ShowProduct.as_view(), name='product-edit'),
        ])),

        path('cart/', include([
            path('', views.Cart.as_view(), name='cart'),
            path('remove-<int:position>/', views.Cart.as_view(), name='cart-remove'),
        ])),

    ]))
]
