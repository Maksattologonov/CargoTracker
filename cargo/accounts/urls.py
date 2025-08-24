from django.urls import path
from .views import logout_view, create_redirect_login_widget, telegram_login_view

urlpatterns = [
    # path('register/', register_view, name='register'),
    path('login/', telegram_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('callback/', callback, name='callback'),
    path('redirect/', create_redirect_login_widget, name='redirect'),
    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    # path('telegram/callback/', telegram_callback, name='telegram_callback'),
]
