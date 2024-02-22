from django.shortcuts import render, redirect, get_object_or_404
from .forms import SorteioForm, ParticipacaoSorteioForm
from .models import Sorteio, ParticipacaoSorteio
import math
import json

from django.contrib import messages

from decimal import Decimal
import re

def home(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'index.html', {'sorteios': sorteios})



def sorteio(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'sorteios/sorteios.html', {'sorteios': sorteios})



def detalhe_sorteio(request, slug):
    sorteio = get_object_or_404(Sorteio, slug=slug)
    maior_numero = sorteio.numero
    digitos = int(math.log10(maior_numero)) + 1 if maior_numero else 1
    numeros = list(range(1, maior_numero + 1))

    # Obter todos os números já selecionados para este sorteio
    participacoes = ParticipacaoSorteio.objects.filter(sorteio=sorteio)
    numeros_selecionados = set()
    for participacao in participacoes:
        numeros_selecionados.update(participacao.numeros_selecionados)

    # Modificar a lógica para incluir o nome do participante
    numeros_reservados_info = {}
    for participacao in participacoes:
        for numero in participacao.numeros_selecionados:
            numeros_reservados_info[numero] = participacao.nome_participante

    # Capturar o número do celular na requisição GET e filtrar os números selecionados
    numero_celular = request.GET.get('verify-number')
    if numero_celular:
        # Certifique-se de que o número do celular está no formato correto
        numero_celular_formatado = numero_celular
        participacoes = ParticipacaoSorteio.objects.filter(sorteio=sorteio, celular_participante=numero_celular_formatado)
        numeros_selecionados = set()
        for participacao in participacoes:
            numeros_selecionados.update(participacao.numeros_selecionados)
        
    # Calcular o número de números livres
    numeros_livres = len(numeros) - len(numeros_selecionados)

    mostrar_popup_modal = 'verify-number' in request.GET

    if request.method == 'POST':
        form = ParticipacaoSorteioForm(request.POST)

        if form.is_valid():
            participacao = form.save(commit=False)
            participacao.sorteio = sorteio

            # Recupere os valores dos campos do formulário
            numeros_selecionados_str = request.POST.get('numeros_selecionados', '')  # Obtenha a string de números selecionados
            numeros_selecionados_str = numeros_selecionados_str.replace(' ', '')  # Remova espaços em branco
            numeros_selecionados_str = numeros_selecionados_str.split(',')  # Divida a string pelos separadores de vírgula
            
            # Converta os números em uma lista de inteiros, ignorando os vazios
            numeros_selecionados_int = [int(num.strip()) for num in numeros_selecionados_str if num.strip()]
            
            nome_participante = request.POST.get('nome_participante')
            celular_participante = request.POST.get('celular_participante')

            try:
                participacao.numeros_selecionados = numeros_selecionados_int
                participacao.nome_participante = nome_participante
                participacao.celular_participante = celular_participante
                participacao.save()
                
                return redirect('detalhe_sorteio', slug=slug)  
            except ValueError:
                print("Erro na conversão dos números selecionados para inteiros")
        else:
            print("Erros do formulário:", form.errors)

    else:
        form = ParticipacaoSorteioForm()

    return render(request, 'sorteios/detalhe_sorteio.html', {
        'sorteio': sorteio, 
        'numeros': numeros, 
        'digitos': digitos, 
        'form': form,
        'numeros_selecionados': numeros_selecionados,
        'numeros_livres': numeros_livres,  # Adicionando a variável numeros_livres ao contexto do template
        'numeros_reservados_info': numeros_reservados_info,

        'mostrar_popup_modal': mostrar_popup_modal,
        'numeros_para_modal': json.dumps(list(numeros_selecionados)),
    })

def adm(request):
    if request.method == 'POST':
        form = SorteioForm(request.POST, request.FILES)

        if form.is_valid():
            sorteio = form.save(commit=False)

            # Obter o valor numérico de 'preco'
            preco_str = request.POST.get('preco')
            # Remover o 'R$ ' do início e substituir ',' por '.'
            preco_str = preco_str.replace('R$ ', '').replace(',', '.')
            # Converter para Decimal
            preco_decimal = Decimal(preco_str)
            sorteio.preco = preco_decimal

            sorteio.save()
            return redirect('home')
        else:
            print("Erros do formulário:", form.errors)
    else:
        form = SorteioForm()

    return render(request, 'admin/adm.html', {'form': form})

