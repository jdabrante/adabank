from django.contrib.auth.models import User
from django.http import HttpRequest

from .models import Profile


class IdAuthBackend:
    def authenticate(self, request: HttpRequest, username=None, password=None) -> User | None:
        try:
            # Pro
            user = Profile.objects.get(identification=username).user
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
