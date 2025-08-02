from django.urls import path
from .views import track, home

urlpatterns = [
    path('track/', track, name='track'),
    path('', home, name='home'),
]
