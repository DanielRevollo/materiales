from django.db import models

from django.contrib.auth.models import User
from venta.apps.principal.models import *
from venta.apps.usuarios.models import *

class Pedido(models.Model):
    cliente=models.ForeignKey(User)
    producto=models.ManyToManyField(producto)
    cantidad=models.IntegerField()
    precio_total=models.FloatField()
    fecha=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.producto

class Carrito(models.Model):
    id_sesion=models.CharField(max_length=200)
    estado=models.BooleanField ( default = False )
    producto=models.ForeignKey(producto)
    cantidad=models.IntegerField()


