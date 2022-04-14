from venv import create
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class APIAccountManager(BaseUserManager):
    def create_user(self, email: str, username:str, password:str=None) -> object:
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must hava a username')
        if not password:
            raise ValueError('Users must hava a password')

        new_user = User.objects.create_user(username, email)
        new_user.set_password(password)
        new_user.save()
        
        return new_user

    def change_password(self, password: str) -> bool:
        self.set_password(password)
        self.save()

        return True 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)