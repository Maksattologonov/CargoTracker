import secrets
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError
from django_telegram_login.widgets.generator import create_redirect_login_widget
from django_telegram_login.widgets.constants import LARGE

from .models import CustomUser


def telegram_login_view(request):
    """Страница с кнопкой входа через Telegram"""
    telegram_login_widget = create_redirect_login_widget(
        redirect_url=settings.TELEGRAM_LOGIN_REDIRECT_URL,
        bot_name=settings.TELEGRAM_BOT_NAME,
        size=LARGE
    )

    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'accounts/login.html', context)


def telegram_callback_view(request):
    """Обработка данных от Telegram после авторизации"""

    # Проверяем наличие данных от Telegram
    if not request.GET.get('hash'):
        return HttpResponse('Отсутствуют данные от Telegram')

    try:
        # Проверяем подлинность данных
        result = verify_telegram_authentication(
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            request_data=request.GET
        )

    except TelegramDataIsOutdatedError:
        return HttpResponse('Данные авторизации устарели (более суток)')

    except NotTelegramDataError:
        return HttpResponse('Данные не от Telegram!')

    # Извлекаем данные пользователя
    tg_id = result['id']
    first_name = result.get('first_name', '')
    last_name = result.get('last_name', '')
    username = result.get('username', '')

    # Создаем или получаем пользователя
    user, created = CustomUser.objects.get_or_create(
        telegram_id=tg_id,
        defaults={
            'username': f"tg_{tg_id}",
            'first_name': first_name,
            'last_name': last_name,
        }
    )

    # Генерируем код доставки, если его нет
    if not user.delivery_code:
        user.delivery_code = secrets.token_hex(8)  # 16 символов
        user.save()

    # Авторизуем пользователя в Django
    login(request, user)

    # Перенаправляем в личный кабинет
    return redirect('dashboard')
