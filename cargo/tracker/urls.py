from django.urls import path
from .views import track, home, calculator

urlpatterns = [
    path('track/', track, name='track'),
    path('calculator/', calculator, name='calculator'),
    path('', home, name='home'),
]
