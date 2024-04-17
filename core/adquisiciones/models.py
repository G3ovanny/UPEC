from django.db import models
from ..base.models import BaseModel
# Create your models here.

class Solicitudes(BaseModel):
    #ubicacion foranea
    # tipo de solicitud bien o servicio (foranea)
    # planificacion planificada/extemporanea (foranea)
    #fecha de solicitud
    #Monto total solicitud de compra
    # Numero de solicitud
    #fecha_recepcion_solicitud
    #centro de costo o unidad organica
    pass

class Proveedores():
    #Ruc
    #Nombre proveedor 
    #Razon Social
    #Direccion
    #Telefono
    #Correo
    pass

class Proforma():
    #numero de proforma
    #forma de pago
    #items foranea
    pass

class Producto():
    #numero de item
    #cantidad
    #cpc
    #unidad
    #descripcion
    #valor unitario
    #valor total
    pass

class Compras():
    #numero de proceso
    # proveedor
    # area requirente unidad organica
    pass

