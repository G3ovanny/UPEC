from django.db import models

# Create your models here.

class BaseModel(models.Model):
    #modelo base del proyecto
    id = models.AutoField(primary_key=True)
    state = models.BooleanField('Estado', default=True)

    #campos que permiten identificar modificaciones de los datos#
    created_date = models.DateTimeField('Fecha de creación',  auto_now=False, auto_now_add=True, null=True, blank= True)
    modified_date = models.DateTimeField('Fecha de modificación', auto_now=True, auto_now_add=False, null=True, blank= True)
    delete_date = models.DateTimeField('Fecha de eliminación',  auto_now=True, auto_now_add=False, null=True, blank= True)

    class Meta:
        abstract = True
        verbose_name = "Modelo Base"
        verbose_name_plural = "Modelos Base"