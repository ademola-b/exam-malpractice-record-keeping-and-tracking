import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import reverse

from institutions.models import InstitutionProfile
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # creates a user with the parameters
        if email is None:
            raise ValueError('Email address is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None):
         # create a superuser with the above parameters

        user = self.create_user(
            email=email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    email = models.CharField(max_length=100, db_index=True,
                             unique=True, verbose_name='email address', blank=True)
    
    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_institution_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def _str_(self):
        return f'{self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    # def get_absolute_url(self):
    #     return reverse("auth:profile", kwargs={
    #         'pk': self.user_id
    #     })

    class Meta:
        db_table = 'User'
        verbose_name_plural = 'Users'