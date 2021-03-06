from django.contrib import admin
from django.urls import path
from core import views # Importando a view
from django.views.generic import RedirectView # com isso conseguimos redirecionar direto na url sem passar por uma view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/', views.lista_eventos), # Criando a path para expor a pagina
    # path('', views.index), # Estamos definindo que se a raiz estiver vazia, chamaremos o index
    path('', RedirectView.as_view(url='/agenda/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('agenda/evento/', views.evento),
    path('agenda/evento/submit', views.submit_evento),
    path('agenda/evento/delete/<int:id_evento>',views.delete_evento), # Estamos passando um id para deletar 
    path('agenda/lista/<int:id_usuario>/', views.json_lista_evento),
]