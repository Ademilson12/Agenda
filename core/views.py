from django.shortcuts import render, redirect  # redirect # importamos o redirect para utilizar no redirecionamento de paginas
from core.models import Evento # Importando Evento para utilização dos models
from django.contrib.auth.decorators import login_required # Decorador para forçar o usuário a logar
from django.contrib.auth import authenticate, login, logout # Importamos os validadores
from django.contrib import messages

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
    evento = Evento.objects.filter(usuario=usuario) # Definindo que eu quero trazer apenas o id 1
    dados = {'eventos':evento} # Dicionário
    return render(request, 'agenda.html', dados) # Trazendo o response que foi configurar como um dicionário