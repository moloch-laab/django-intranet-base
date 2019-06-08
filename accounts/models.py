from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self, rut, email=None, full_name=None, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not rut:
            raise ValueError("El usuario debe tener RUT")
        if not password:
            raise ValueError("El usuario debe tener contraseña")
        user_obj = self.model(rut = rut)
        user_obj.full_name = full_name
        user_obj.email = self.normalize_email(email)
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, rut, email=None, full_name=None, password=None):
        user = self.create_user(
                rut,
                email,
                full_name=full_name,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, rut, email=None, full_name=None, password=None):
        user = self.create_user(
                rut,
                email,
                full_name=full_name,
                password=password,
                is_staff=True,
                is_superuser=True
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):
    rut         = models.CharField(max_length=20, unique=True)
    email       = models.EmailField(max_length=255, blank=True, null=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    active      = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    superuser   = models.BooleanField(default=False) # superuser 
    timestamp   = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'rut' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.rut

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.rut

    def get_short_name(self):
        return self.rut

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active

