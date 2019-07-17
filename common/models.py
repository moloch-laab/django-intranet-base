from django.db import models
import time
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from core.utils import valida_rut

class UserManager(BaseUserManager):
    """ Crea y almacena users, staffusers y superusers """
    
    def create_user(self, rut, email=None, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_superuser=False, profile_pic=None):
        if not rut:
            raise ValueError("El usuario debe tener RUT")
        if not password:
            raise ValueError("El usuario debe tener contraseña")
        if not valida_rut(rut):
            raise ValueError("Rut no válido")
        user_obj = self.model(rut = rut)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = self.normalize_email(email)
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        user_obj.active = is_active
        user_obj.profile_pic = profile_pic
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, rut, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(
                rut,
                email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, rut, email=None, first_name=None, last_name=None, password=None):
        user = self.create_user(
                rut,
                email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_staff=True,
                is_superuser=True
        )
        return user

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)

class User(SimpleEmailConfirmationUserMixin, AbstractBaseUser, PermissionsMixin):
    """ Los usuarios dentro del sistema de autenticación de Django están
    representados por este model.
    
    Los campos email, rut y password son obligatorios """

    file_prepend = "users/profile_pics"
    rut          = models.CharField(max_length=20, unique=True)
    email        = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    first_name   = models.CharField(max_length=255, blank=True, null=True)
    last_name    = models.CharField(max_length=255, blank=True, null=True)
    active       = models.BooleanField(default=True) # can login 
    staff        = models.BooleanField(default=False) # staff user non superuser
    superuser    = models.BooleanField(default=False) # superuser 
    timestamp    = models.DateTimeField(auto_now_add=True)
    profile_pic  = models.ImageField(max_length=1000, upload_to=img_url, null=True, blank=True)

    USERNAME_FIELD = 'rut' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['email'] #['full_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        else:
            full_name = self.email
        return full_name

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

