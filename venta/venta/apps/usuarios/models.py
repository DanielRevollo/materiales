from django.db import models
from django.contrib.auth.models import User


class perfil_user(models.Model):
    user = models.OneToOneField(User)
    nombre=models.CharField(max_length='100', verbose_name='Nombre')
    ap_paterno=models.CharField(max_length='100', verbose_name='Apellido Paterno')
    ap_materno=models.CharField(max_length='100', verbose_name='Apellido Materno')
    CI_NIT= models.IntegerField(verbose_name='CI/NIT',max_length='11')
    email=models.EmailField(verbose_name='E-mail')
    user= models.ForeignKey(User,null=True, blank=True)
    def __unicode__(self):
        return self.user
    class Meta:
        verbose_name_plural='perfil usuario'
