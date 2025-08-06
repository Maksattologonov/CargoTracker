from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django_telegram_login.widgets.constants import SMALL
from django_telegram_login.widgets.generator import create_callback_login_widget
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserRegisterForm
from django_telegram_login.widgets.constants import (
    SMALL,
    MEDIUM,
    LARGE,
    DISABLE_USER_PHOTO,
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL

telegram_login_widget = create_callback_login_widget(bot_name, corner_radius=10, size=MEDIUM)

telegram_login_widget = create_redirect_login_widget(
    redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неверный email или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def create_redirect_login_widget(size=SMALL, user_photo=True, access_write=True
):
    """
    Create redirect widget, that allows to handle user data as get request params.
    """
    script_initital = \
        '<script async src="https://telegram.org/js/telegram-widget.js?2" '
    bot = 'data-telegram-login="{}" '.format(bot_name)
    size = 'data-size="{}" '.format(size)
    userpic = \
        'data-userpic="{}" '.format(str(user_photo).lower()) if not user_photo else ''
    redirect = 'data-auth-url="{}" '.format(redirect_url)
    access = 'data-request-access="write"' if access_write else ''
    script_end = '></script>'

    widget_script = \
        script_initital + bot + size + userpic + redirect + access + script_end
    return widget_script


def callback(request):
    telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'accounts/callback.html', context)
