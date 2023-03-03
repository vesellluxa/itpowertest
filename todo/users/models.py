from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class ToDoUserManager(BaseUserManager):
    def create_user(self,
                    email,
                    password,
                    first_name=None,
                    last_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         password):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ToDoUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address",
                              unique=True)
    first_name = models.CharField(verbose_name="first name",
                                  max_length=150,
                                  null=True)
    last_name = models.CharField(verbose_name="last name",
                                 max_length=150,
                                 null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = ToDoUserManager()
