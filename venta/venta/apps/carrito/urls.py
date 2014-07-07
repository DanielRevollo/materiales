from django.conf.urls import patterns, url
from views import *
urlpatterns=patterns("",
    url(r'^productos/$',productos),
    url(r'^productos/mostrar/carrito/$',carrito_mostrar),
    url(r'^productos/cargar/carrito/(\d+)/$',cargar_carrito),
    url(r'^productos/carrito/add/(\d+)/$',carrito_add),
    url(r'^carrito/eliminar/(?P<id>\d+)/$',eliminar_de_carrito),
    url(r'^producto/(?P<id>\d+)/$',listar_producto),
    url(r'^confirmar/compra/$',confirmar_compra),
    url(r'^producto/comprar/final/$',realizar_transaccion),
    )