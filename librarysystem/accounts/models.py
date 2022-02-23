from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    username = None 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    total_book_due = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between if set, otherwise the email address.
        """
        full_name = f'{self.first_name} {self.last_name}'.strip()

        if not full_name:
            full_name = self.email

        return full_name

    def get_short_name(self):
        """
        :return: Returns the short name for the user
        """
        return self.first_name

