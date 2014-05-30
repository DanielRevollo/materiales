from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

#lo que isimos por el email
from django.core.mail import EmailMultiAlternatives
from venta.apps.usuarios.forms import *
#lo que isismos por el email
from venta.apps.usuarios.models import *
from venta.apps.usuarios.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,permission_required


def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        formularioPerfil=perfil_userForm(request.POST,request.FILES)
        if formulario.is_valid() and formularioPerfil.is_valid():
            u = formulario.save()
            perfil = formularioPerfil.save()
            perfil.user=u

            perfil.per_user=perfil
            perfil.save()
        return HttpResponseRedirect('/')
    else:
        formulario = UserCreationForm()
        formularioPerfil=perfil_userForm()
    return render_to_response('new_user.html',{'formulario':formulario,'formularioPerfil':formularioPerfil}, context_instance=RequestContext(request))


def login_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form =LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['passsword']

                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx ={'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def contacto(request):
    info_enviado = False
    email = ""
    titulo = ""
    texto = ""
    if request.method == "POST":
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']
            to_admin = 'ocamporoberto97@gmail.com'
            html_content = "Informacion recibida de [%s]<br><br><br>***Mensaje***<br><br>%s" % (email, texto)
            msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com', [to_admin])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    else:
        formulario = ContactoForm()
    ctx = {'form': formulario, "email": email, "titulo": titulo, "texto": texto, "info_enviado": info_enviado}
    return render_to_response('contactoform.html', ctx, context_instance=RequestContext(request))
