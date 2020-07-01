from django.urls import path
from . import views

app_name = 'websites'

urlpatterns = [
    path('<url>/', views.Home.as_view(), name='home'),
    path('<url>/<category>/', views.Home.as_view(), name='category')
]
