
""" ENVIO DE SMS """
"""
def send_test_sms(request):
    # Aqui você pode usar a função format_number_for_sms se necessário
    formatted_number = format_number_for_sms('(123) 456-7890')
    result = send_sms_via_textbelt(formatted_number, 'Olá, este é um teste de SMS do Django!')"""



# utils.py

import requests
from django.conf import settings

def send_sms_via_textbelt(to, message):
    response = requests.post('https://textbelt.com/text', {
        'phone': to,
        'message': message,
        'key': settings.TEXTBELT_API_KEY,
    })
    return response.json()

def format_number_for_sms(number):
    return '+1' + number.translate(str.maketrans('', '', '()- '))



views pagamento:

# Enviar SMS após o pagamento
            celular_participante = request.POST.get('celular_participante')
            if celular_participante:
                celular_participante_formatado = format_number_for_sms(celular_participante)
                mensagem_pagamento = "Obrigado por efetuar o pagamento."
                #send_sms_via_textbelt(celular_participante_formatado, mensagem_pagamento)
            

views participações:

 # Enviar SMS após a participação
                celular_participante = participacao.celular_participante
                nome_participante = participacao.nome_participante
                mensagem_participacao = f"Parabéns, {nome_participante}, por escolher seus números. Acesse o site para efetuar o pagamento."
                celular_participante_formatado = format_number_for_sms(celular_participante)
                #send_sms_via_textbelt(celular_participante_formatado, mensagem_participacao)
