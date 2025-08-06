# telegram_auth.py
from django.contrib.auth import get_user_model
from django.db import transaction
from telegram import Update
from telegram.ext import CallbackContext

User = get_user_model()


def handle_telegram_login(update: Update, context: CallbackContext):
    """Link a Telegram user to a site account using an auth key.

    The user should send their unique ``auth_key`` to the bot. If a matching
    account is found, the Telegram ``id`` is stored on the user model and the
    bot confirms the successful authentication. Otherwise an error message is
    sent.
    """
    telegram_user = update.effective_user
    auth_key = (update.message.text or '').strip()

    with transaction.atomic():
        try:
            user = User.objects.select_for_update().get(auth_key=auth_key)
            user.telegram_id = telegram_user.id
            user.save(update_fields=["telegram_id"])
            context.bot.send_message(
                chat_id=telegram_user.id,
                text="Вы успешно авторизовались."
            )
            return user
        except User.DoesNotExist:
            context.bot.send_message(
                chat_id=telegram_user.id,
                text="Неверный код авторизации."
            )
            return None
