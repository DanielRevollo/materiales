from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'venta.views.home', name='home'),
    # url(r'^venta/', include('venta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'venta.apps.principal.views.home'),

    #esta dirccion es importante para que te cargue las imagenes subidas
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),

    #registro categoria y registro de producto
    url(r'^producto/nueva/$','venta.apps.principal.views.create_producto'),
    url(r'^categoria/nueva/$','venta.apps.principal.views.new_categ'),


    #usuario
    url(r'^usuario/new/$', 'venta.apps.usuarios.views.nuevo_usuario'),

    # logeo de usuarios
    url(r'^login/$','venta.apps.usuarios.views.login_view',name='vista_login'),
    url(r'^logout/$','venta.apps.usuarios.views.logout_view',name='vista_logout'),
    url(r'^verificar/usuario/$','venta.apps.usuarios.views.verificar'),

    url(r'^usuario/update_usuario/(?P<id>\d+)/$', 'venta.apps.usuarios.views.update_usuario'),

    #LISTAD DE PRODUCTOS Y CATEGORIAS

    url(r'^categorias/$','venta.apps.principal.views.lista_categorias'),
    url(r'^productos_lista/$','venta.apps.principal.views.lista_productos'),
    url(r'^listado/(?P<categoria>\d+)/$','venta.apps.principal.views.lista_por_categorias'),

    # MODIFICACION DE PRODUCTOS
    url(r'^principal/update/(?P<id_prod>\d+)/$', 'venta.apps.principal.views.update_produc'),
    #CONTACTANOS
    url(r'^contacto/$','venta.apps.usuarios.views.contacto'),

    #CARRITO DE VENTAS
    url(r'^',include("venta.apps.carrito.urls")),
    #===================================================================
    url(r'^reportes/$','venta.apps.carrito.views.vista_reporte'),
    url(r'^reporte/filtro/$','venta.apps.principal.views.reporteFiltro'),
    url(r'^reporte_productos/$','venta.apps.principal.views.crearReporte'),
    url(r'^reporte_venta/$','venta.apps.carrito.views.ReporteVentas'),


    # urls de la busqueda
    url(r'^resultdos/$','venta.apps.principal.views.buscarProducto'),

    #======================FACTURA=========================
    url(r'^factura/(?P<id_venta>\d+)/$', 'venta.apps.carrito.views.factura'),
    url(r'^usuarios/$', 'venta.apps.usuarios.views.re_usuario'),
    url(r'^codigo/(?P<id>\d+)/$', 'venta.apps.carrito.views.geneFactura'),
)

