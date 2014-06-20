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

    #LISTAD DE PRODUCTOS Y CATEGORIAS

    url(r'^categorias/$','venta.apps.principal.views.lista_categorias'),
    url(r'^productos/$','venta.apps.principal.views.lista_productos'),

    # MODIFICACION DE PRODUCTOS
    url(r'^principal/update/(?P<id_prod>\d+)/$', 'venta.apps.principal.views.update_produc'),
    #CONTACTANOS
    url(r'^contacto/$','venta.apps.usuarios.views.contacto'),

    #CARRITO DE VENTAS
    url(r'^carrito/new/(?P<venta_id>\d+)/$', 'venta.apps.carrito.views.new_venta'),
    url(r'^carrito/cantidad/(?P<id_venta>\d+)/(?P<id_pro>\d+)/$', 'venta.apps.carrito.views.new_cantidad'),
    url(r'^carrito/confirmar/(?P<id_venta>\d+)/$', 'venta.apps.carrito.views.confirmar'),
    #url(r'^carrito/factura/$', 'carrito.views.factura'),


)

