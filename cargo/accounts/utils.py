# auth_key_generator.py
from django.contrib.auth import get_user_model
from django.db import transaction


def generate_next_auth_key():
    """Return the next unique auth key.

    Using ``get_user_model`` avoids a direct import of ``CustomUser`` which
    would otherwise create a circular import between the model and this
    utility module.
    """
    user_model = get_user_model()
    with transaction.atomic():
        # Блокируем таблицу для предотвращения race condition
        last_user = user_model.objects.select_for_update().order_by('-auth_key').first()

        if not last_user:
            return 'C0001'

        current_key = last_user.auth_key
        return calculate_next_key(current_key)


def calculate_next_key(s: str) -> str:
    if s == 'ZZZZZ':
        raise ValueError("Maximum key limit reached")

    # Разделяем на буквы и цифры
    alpha_part = []
    num_part = []
    for c in s:
        if c.isalpha():
            alpha_part.append(c)
        else:
            num_part.append(c)

    if num_part:
        # Увеличиваем числовую часть
        num_str = ''.join(num_part)
        num = int(num_str) + 1
        if num <= 10 ** len(num_part) - 1:
            new_num = str(num).zfill(len(num_part))
            return ''.join(alpha_part) + new_num

    # Если числовая часть переполнена, увеличиваем буквенную
    new_alpha = increment_alpha(''.join(alpha_part))
    if not new_alpha:
        # Если буквенная часть переполнена, расширяем формат
        new_alpha_len = len(alpha_part) + 1
        if new_alpha_len > 5:
            raise ValueError("Maximum key length exceeded")
        new_alpha = 'C' + 'A' * (new_alpha_len - 1)

    # Определяем длину числовой части для нового формата
    num_length = 5 - len(new_alpha)
    return new_alpha + '1'.zfill(num_length)


def increment_alpha(s: str) -> str:
    chars = list(s)
    carry = 1
    for i in range(len(chars) - 1, -1, -1):
        if carry == 0:
            break
        char = chars[i]
        new_char_ord = ord(char) + carry
        if new_char_ord > ord('Z'):
            chars[i] = 'A'
            carry = 1
        else:
            chars[i] = chr(new_char_ord)
            carry = 0

    if carry:
        return None
    return ''.join(chars)
