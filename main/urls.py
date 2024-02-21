from django.urls import path
from .views import home, sorteio, adm, detalhe_sorteio



urlpatterns = [

    path('', home, name='home' ),
    path('sorteios/', sorteio, name='sorteio'),
    path('sorteio/<slug:slug>/', detalhe_sorteio, name='detalhe_sorteio'),
    path('administracao/', adm, name='adm'),
]