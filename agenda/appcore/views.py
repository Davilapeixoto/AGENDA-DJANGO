from django.shortcuts import render, redirect
from appcore.models import Evento
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return  redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha invalido")
            return redirect('/')
    else:
        redirect('/')

#def index(request):
#    return redirect('/agenda/')
@login_required(login_url='/login/')
def lista_evento(request):
    user = request.user
    if user.is_superuser:
        evento = Evento.objects.all()
    else:
        evento = Evento.objects.filter(usuario=user)
    #usuario= request.user
    #evento = Evento.objects.filter(usuario=usuario)
    #evento = Evento.objects.all()
    dad = {'eventos': evento}
    return render(request, 'agenda.html', dad)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    print(id_evento)
    dados ={}
    if id_evento:
        dados['evento']= Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo =titulo, data_evento =data_evento, descricao =descricao)
        else:
            Evento.objects.create(titulo =titulo, data_evento =data_evento, descricao =descricao,usuario =usuario )

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')