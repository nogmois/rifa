from django.urls import path
from .views import home, sorteio, adm, detalhe_sorteio, excluir_sorteio, participantes_json, alterar_horas, send_test_sms



urlpatterns = [

    path('', home, name='home' ),
    path('sorteios/', sorteio, name='sorteio'),
    path('sorteio/<slug:slug>/', detalhe_sorteio, name='detalhe_sorteio'),
    path('administracao/<slug:slug>/', adm, name='adm'),
    path('administracao/', adm, name='adm'),
    
    path('sorteio/excluir/<slug:slug>/', excluir_sorteio, name='excluir_sorteio'),
    path('participantes-json/', participantes_json, name='participantes_json'),
    # urls.py
    path('alterar-horas/<int:participacao_id>/', alterar_horas, name='alterar_horas'),

    # sms
    path('send-sms/', send_test_sms, name='send_test_sms'),
]