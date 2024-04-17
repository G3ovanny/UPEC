from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from simple_history.models import HistoricalRecords

# Create your models here.


class UserManager(BaseUserManager):
    def _create_user(self, username, correo, nombre, apellido_paterno, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            correo = correo,
            nombre = nombre,
            apellido_paterno = apellido_paterno,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, correo, nombre, apellido_paterno, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido_paterno, password, False, False, **extra_fields)
    
    def create_superuser(self, username, correo, nombre, apellido_paterno, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido_paterno, password, True, True, **extra_fields)
    

class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, blank=True, null= True, unique=True)
    clave_temporal = models.BooleanField(default=True)
    fecha_clave = models.DateField('Fecha cambio contraseña', auto_now=True, blank=True, null=True)
    password = models.CharField('password', max_length=255, blank=True, null= True, unique=True)
    correo = models.EmailField('Correo electrónico', max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, null=True, blank= True, verbose_name= 'Nombre Usuario')
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellido Paterno")
    tipoUsuario = models.IntegerField('Tipo de usuario', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    historical = HistoricalRecords()
    objects = UserManager()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        db_table = "Usuarios"
        ordering =['id']


    USERNAME_FIELD= 'username'
    REQUIRED_FIELDS = ['correo', 'nombre', 'apellido_paterno']

    def __str__(self):
        return f'{self.nombre}'