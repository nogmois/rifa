from django.urls import path
from .views import home, sorteio, adm, detalhe_sorteio, excluir_sorteio



urlpatterns = [

    path('', home, name='home' ),
    path('sorteios/', sorteio, name='sorteio'),
    path('sorteio/<slug:slug>/', detalhe_sorteio, name='detalhe_sorteio'),
    path('administracao/<slug:slug>/', adm, name='adm'),
    path('administracao/', adm, name='adm'),
    
    path('sorteio/excluir/<slug:slug>/', excluir_sorteio, name='excluir_sorteio'),
]