from django.db import models

from django.contrib.auth.models import User
from venta.apps.principal.models import *
from venta.apps.usuarios.models import *

class Venta(models.Model):
    costo_total = models.FloatField(default='0.0')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(User, null = True, blank = True)
    estado = models.BooleanField(default=False)
    def __unicode__(self):
        return self.cliente.username
    class Meta:
        ordering = ['fecha_venta']
        verbose_name_plural = "Ventas"

class DetalleVenta(models.Model):
    cantidad = models.IntegerField()
    costo_producto = models.FloatField()
    producto = models.ForeignKey(producto)
    venta = models.ForeignKey(Venta)
    def __unicode__(self):
        return self.producto.nombre_pro
    class Meta:
        verbose_name_plural = "Detalle Venta"
        ordering = ['producto']

class factura(models.Model):
    NIT_institu= models.IntegerField(verbose_name='NIT de la Institucion',max_length='10',default='0194826659', null=False,unique=True)
    det_compra= models.CharField(verbose_name='Detalle de compra', max_length='100')
    Nro_autorizacion=models.IntegerField(verbose_name='Numero de autoriacion', default='500400753825', unique=True)
    compras=models.ForeignKey(Venta)
    def __unicode__(self):
        return self.NIT_institu
    class Meta:
        ordering=['Nro_autorizacion']
