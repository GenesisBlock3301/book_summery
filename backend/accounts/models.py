import logging
import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def create_user(self, username=None, password=None):
        """
        Create general user method
        """
        if not username:
            raise ValueError('Email or Username must be specified!')

        if self.is_valid_email(username):
            user = self.model(email=self.normalize_email(username),)
        else:
            user = self.model(username=username)
        user.set_password(password)
        user.save(self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """
            Create superuser method
        """
        if not email:
            raise ValueError('Email must be specified!')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(self._db)
        return user


class User(AbstractBaseUser):
    """Custom user model"""
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=255, null=True, unique=True) 
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=100, blank=True, default="self")

    USERNAME_FIELD = "email"
    
    class Meta:
        index_together = ("username", "email")

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email if self.email else self.username

