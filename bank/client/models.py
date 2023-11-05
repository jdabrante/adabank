from django.conf import settings
from django.db import models


class Profile(models.Model):
    identification = models.CharField(max_length=9, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    avatar = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self) -> str:
        return f'Profile of {self.user.username}'
