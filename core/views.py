from django.contrib.auth.models import User
from django.shortcuts import render, redirect  # redirect # importamos o redirect para utilizar no redirecionamento de paginas
from core.models import Evento # Importando Evento para utilização dos models
from django.contrib.auth.decorators import login_required # Decorador para forçar o usuário a logar
from django.contrib.auth import authenticate, login, logout # Importamos os validadores
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.

#def index(request): # Quando não for informado o index, ele vai ser redirecionado para agenda
#    return redirect('/agenda/') 

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username') # Estou recuperando o arquivo que foi me passado pelo form
        password = request.POST.get('password') # Estou recuperando o arquivo que foi me passado pelo form
        usuario = authenticate(username=username, password=password)
        if usuario is not None: # Se o usuário não for none ele vai logar e retornar para o indice
            login(request, usuario)
            return redirect ('/') # Retorna para o indice
        else:
            messages.error(request, "Usuário ou senha invalido") # Se não conseguir fazer o submit ele cai nessa mensagem
            return redirect('/') # Caso não venha pela url, vai ser redirecionado para pagina de login

@login_required(login_url='/login/') # Para que as informações abaixo sejam apresentadas você precisa estar logado
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=2)
    evento = Evento.objects.filter(usuario=usuario,
                                    data_evento__gt=data_atual) # Definindo que eu quero trazer apenas o id 1
    dados = {'eventos':evento} # Dicionário
    return render(request, 'agenda.html', dados) # Trazendo o response que foi configurar como um dicionário

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {} # Dicionário vazio para receber o evento
    if id_evento: 
        dados['evento'] = Evento.objects.get(id=id_evento) # Se ele encontrar informações no objeto evento ele vai preecher com os dados
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        id_evento = request.POST.get('id_evento')
        
        if id_evento: # Se o id do evento existir, ele faz as verificações abaixo
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento 
                evento.save()
        
        #if id_evento: # Se o evento existir ele vai editar os dados, manter o id e salvar
        #    Evento.objects.filter(id=id_evento).update(titulo=titulo,
        #                                            data_evento=data_evento,
        #                                            descricao=descricao)    
        
        else: # Se não existir ele vai criar um novo evento com um novo id
            Evento.objects.create(titulo=titulo,
                                data_evento=data_evento,
                                descricao=descricao,
                                usuario=usuario)
    return redirect('/')   

@login_required(login_url='/login/')
def delete_evento(request, id_evento): # Recebe um request e o id do evento
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento) # Informa o id do evento e manda o delete
    except Exception:
        raise Http404()
    if usuario == evento.usuario: # Validação para verificar se o usuário é dono do evento para deleção
        evento.delete() # Caso o usuário seja o criador do evento ele vai deletar
    else:
        raise Http404()            
    return redirect('/')  # Retorna para página principal


def json_lista_evento(request, id_usuario):
    try:
        usuario = User.objects.get(id=id_usuario)
        evento = Evento.objects.filter(usuario=usuario).values('id','titulo') # Informando quais arquivos quero mostrar no formato js
        return JsonResponse(list(evento), safe=False)
    except Exception:
        raise Http404()
    return redirect('/')
    
    