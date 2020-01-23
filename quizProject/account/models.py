from django.db import models , IntegrityError

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, default='user')
    active = models.BooleanField(default=True)
    quiz_creator = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = BaseUserManager()

    @staticmethod
    def create_user(username, password):
        user = CustomUser(username = username, password = password)
        user.set_password(password)
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            return None

    def __str__(self):
        return f'username: {self.username}, {self.email}'

    def get_username(self):
        return self.username

    @property
    def is_stuff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_quiz_creator(self):
        return self.quiz_creator


# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, is_active=True, is_admin=False, is_stuff=False):
#         if not username:
#             raise ValueError('Users must have an username')
#         if not password:
#             raise ValueError('Users must have password')
#
#         user = self.model(
#
#         )