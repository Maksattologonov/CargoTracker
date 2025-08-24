from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import hashlib
import hmac
import json
import time

# Telegram Login Widget
from django_telegram_login.widgets.constants import (
    SMALL, MEDIUM, LARGE, DISABLE_USER_PHOTO
)
from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError,
    TelegramDataIsOutdatedError,
)


def telegram_login_view(request):
    """Страница с Telegram Login Widget"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Генерируем виджет для callback авторизации
    telegram_login_widget = create_callback_login_widget(
        bot_name=settings.TELEGRAM_BOT_NAME,
        size=LARGE,
        corner_radius=10,
        user_photo=True
    )

    # Альтернативно - redirect виджет
    # telegram_login_widget = create_redirect_login_widget(
    #     redirect_url=request.build_absolute_uri('/telegram-auth/'),
    #     bot_name=settings.TELEGRAM_BOT_NAME,
    #     size=LARGE,
    #     user_photo=DISABLE_USER_PHOTO
    # )

    context = {
        'telegram_login_widget': telegram_login_widget
    }
    return render(request, 'accounts/login.html', context)


@csrf_exempt
def telegram_auth_callback(request):
    """Обработка callback от Telegram Login Widget (AJAX)"""
    if request.method == 'POST':
        try:
            # Получаем данные из POST запроса
            data = json.loads(request.body)

            # Проверяем подлинность данных от Telegram
            result = verify_telegram_authentication(
                bot_token=settings.TELEGRAM_BOT_TOKEN,
                request_data=data
            )

            # Создаем или получаем пользователя
            user = get_or_create_telegram_user(result)

            if user and user.is_active:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': f'Добро пожаловать, {user.first_name}!',
                    'redirect_url': '/dashboard/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Аккаунт деактивирован'
                }, status=400)

        except TelegramDataIsOutdatedError:
            return JsonResponse({
                'success': False,
                'error': 'Данные авторизации устарели'
            }, status=400)
        except NotTelegramDataError:
            return JsonResponse({
                'success': False,
                'error': 'Неверные данные от Telegram'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка авторизации: {str(e)}'
            }, status=500)

    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'}, status=405)


def telegram_auth_redirect(request):
    """Обработка redirect от Telegram Login Widget"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Проверяем, есть ли данные от Telegram в GET параметрах
    if not request.GET.get('hash'):
        messages.error(request, 'Отсутствуют данные авторизации от Telegram')
        return redirect('telegram_login')

    try:
        # Проверяем подлинность данных
        result = verify_telegram_authentication(
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            request_data=request.GET
        )

        # Создаем или получаем пользователя
        user = get_or_create_telegram_user(result)

        if user and user.is_active:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Аккаунт деактивирован')

    except TelegramDataIsOutdatedError:
        messages.error(request, 'Данные авторизации получены более суток назад')
    except NotTelegramDataError:
        messages.error(request, 'Данные не связаны с Telegram!')
    except Exception as e:
        messages.error(request, f'Ошибка авторизации: {str(e)}')

    return redirect('telegram_login')


def get_or_create_telegram_user(telegram_data):
    """Создает или получает пользователя по данным Telegram"""
    telegram_id = telegram_data.get('id')
    first_name = telegram_data.get('first_name', '')
    last_name = telegram_data.get('last_name', '')
    username = telegram_data.get('username', '')
    photo_url = telegram_data.get('photo_url', '')

    try:
        # Пытаемся найти пользователя по Telegram ID
        from .models import TelegramUser
        telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
        user = telegram_user.user

        # Обновляем данные пользователя
        user.first_name = first_name
        user.last_name = last_name
        if username and not User.objects.filter(username=username).exclude(id=user.id).exists():
            user.username = username
        user.save()

        # Обновляем данные Telegram
        telegram_user.first_name = first_name
        telegram_user.last_name = last_name
        telegram_user.username = username
        telegram_user.photo_url = photo_url
        telegram_user.save()

        return user

    except TelegramUser.DoesNotExist:
        # Создаем нового пользователя
        username_base = username or f"telegram_{telegram_id}"
        username_final = username_base

        # Проверяем уникальность username
        counter = 1
        while User.objects.filter(username=username_final).exists():
            username_final = f"{username_base}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username_final,
            first_name=first_name,
            last_name=last_name,
            email=''  # Telegram не предоставляет email
        )

        # Создаем связь с Telegram
        from .models import TelegramUser
        TelegramUser.objects.create(
            user=user,
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            photo_url=photo_url
        )

        return user


@login_required
def dashboard(request):
    """Главная страница для авторизованных пользователей"""
    try:
        telegram_user = request.user.telegramuser
        context = {
            'telegram_data': {
                'first_name': telegram_user.first_name,
                'last_name': telegram_user.last_name,
                'username': telegram_user.username,
                'photo_url': telegram_user.photo_url,
            }
        }
    except:
        context = {}

    return render(request, 'dashboard.html', context)


@login_required
def logout_view(request):
    """Выход из системы"""
    username = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'До свидания, {username}!')
    return redirect('telegram_login')


# Дополнительная функция для ручной проверки Telegram данных
def verify_telegram_hash(data, bot_token):
    """
    Проверка подлинности данных от Telegram
    Альтернативная реализация если django-telegram-login не работает
    """
    received_hash = data.get('hash')
    if not received_hash:
        return False

    # Убираем hash из данных
    auth_data = {k: v for k, v in data.items() if k != 'hash'}

    # Сортируем ключи и создаем строку для проверки
    auth_data_str = '\n'.join([f'{k}={v}' for k, v in sorted(auth_data.items())])

    # Создаем секретный ключ из токена бота
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    # Вычисляем HMAC
    calculated_hash = hmac.new(
        secret_key,
        auth_data_str.encode(),
        hashlib.sha256
    ).hexdigest()

    return calculated_hash == received_hash
