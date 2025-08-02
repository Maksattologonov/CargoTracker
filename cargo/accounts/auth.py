# telegram_auth.py
from django.contrib.auth import get_user_model
from telegram import Update
from telegram.ext import CallbackContext

User = get_user_model()


def handle_telegram_login(update: Update, context: CallbackContext):
    telegram_user = update.effective_user

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            telegram_id=telegram_user.id,
            defaults={
                'username': f"tg_{telegram_user.id}",
                'first_name': telegram_user.first_name,
                'last_name': telegram_user.last_name,
            }
        )

        if created:
            context.bot.send_message(
                chat_id=telegram_user.id,
                text=f"Ваш ключ доступа: {user.auth_key}\n"
                     f"Используйте его для входа в систему."
            )
        else:
            context.bot.send_message(
                chat_id=telegram_user.id,
                text=f"Добро пожаловать назад! Ваш ключ: {user.auth_key}"
            )

    return user