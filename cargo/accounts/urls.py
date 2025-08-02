from django.urls import path
from .views import register_view, login_view, logout_view, callback, create_redirect_login_widget

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('callback/', callback, name='callback'),
    path('redirect/', create_redirect_login_widget, name='redirect'),
]
