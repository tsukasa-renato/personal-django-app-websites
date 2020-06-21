from django.urls import path
from . import views

urlpatterns = [
    path('<url>/', views.Home.as_view(), name='home'),
]
