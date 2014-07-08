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



class factura(models.Model):
    N_Autorizacion=models.CharField(max_length=15,verbose_name="N_autorizacion")
    llave=models.CharField(max_length=20,verbose_name="llave")
    Dato=models.ForeignKey(Pedido)
    nit=models.ForeignKey(perfil_user)
    def __unicode__(self):
        return self.N_Autorizacion

