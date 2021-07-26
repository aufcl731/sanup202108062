from django.conf import settings
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.base_user import BaseUserManager

#def propic_upload_path(instance, filename):
#    return '/'.join(['user', str(instance.id), filename])

class Department(models.Model):
    name = models.CharField(max_length=25)


class Company(models.Model):
    name = models.CharField(max_length=25)
    code = models.CharField(max_length=100, null=True)
    num = models.CharField(max_length=20 ,null=True)
    machineyn = models.BooleanField(default=True)
    x = models.IntegerField(null=True, default=None)
    y = models.IntegerField(null=True, default=None)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        #help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(max_length=20)
    company_code = models.ForeignKey(Company, null=True ,on_delete=models.CASCADE)
    level = models.IntegerField(null=True, default=0)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    group_code = models.ForeignKey(Department, null=True ,on_delete=models.CASCADE)
    theme_code = models.IntegerField(default=0)
    lang_code = models.IntegerField(default=0)
    propic = models.ImageField(upload_to='data/user/', null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

class Account(models.Model):
    accountname = models.CharField(max_length=30, null=False)
    accountmanager = models.CharField(max_length=100, null=True)
    accountwork = models.CharField(max_length=100, null=True)
    accounttype = models.CharField(max_length=100, null=True)
    accountnum = models.CharField(max_length=100,null=False)
    accountaddress = models.CharField(max_length=100, null=True)

