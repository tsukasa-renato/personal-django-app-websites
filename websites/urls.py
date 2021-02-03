from django.urls import path, include
from .views import *
from .apis import urls

app_name = 'websites'

urlpatterns = [
    path('api/', include(urls.urlpatterns)),
    path('<slug:url>/', include([

        path('', ShowProducts.as_view(), name='home'),
        path('c/<slug:selected_category>/', ShowProducts.as_view(), name='category'),

        path('p/<slug:selected_product>/', include([
            path('', ShowProduct.as_view(), name='product'),
            path('edit-<int:position>/', ShowProduct.as_view(), name='product-edit'),
        ])),

        path('cart/', include([
            path('', Cart.as_view(), name='cart'),
            path('add/', CartActions.as_view(), name='cart-add'),
            path('remove-<int:position>/', CartActions.as_view(), name='cart-remove'),
        ])),

    ]))
]
