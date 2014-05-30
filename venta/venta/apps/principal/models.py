from django.db import models

class categoria(models.Model):
    nombre_cat=models.CharField(max_length='100',verbose_name='Nombre de categoria')
    def __unicode__(self):
    	return self.nombre_cat
    class Meta:
    	verbose_name_plural='Categoria de Productos'
        ordering=['nombre_cat']

class producto(models.Model):
    nombre_pro=models.CharField(max_length='100',verbose_name='Nombre de Producto')
    Precio=models.FloatField(null= True)
    descripcion=models.TextField(verbose_name='descripcion')
    portada=models.ImageField(upload_to='portada', null=True)
    estado=models.BooleanField(default=True)
    nom_categoria=models.ForeignKey(categoria)

    def __unicode__(self):
    	return self.nombre_pro
    class Meta:
    	verbose_name_plural='Productos Registrados'
        ordering=['nombre_pro']

class stock(models.Model):
    fecha_ing = models.DateField(verbose_name='Fecha de Registro',auto_now_add=True)
    cantidad= models.IntegerField(verbose_name='Cantidad de Producto')
    reg_pro=models.ForeignKey(producto, null=True, blank=True)
    def __unicode__(self):
        return self.fecha_venc
    class Meta:
        verbose_name_plural='stock  de producto'
        ordering=['fecha_ing']
