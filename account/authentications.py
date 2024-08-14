from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from account.models import User


class CustomUserAuthentication(BaseBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        login_valid = settings.ADMIN_LOGIN == username
        psw_valid = settings.ADMIN_PASSWORD == password
        if login_valid and psw_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_admin = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
