# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from models import CustomUser

class TelegramAuthKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_key = request.headers.get('X-Auth-Key')
        if not auth_key:
            return None

        try:
            user = CustomUser.objects.get(auth_key=auth_key)
            return (user, None)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid auth key')