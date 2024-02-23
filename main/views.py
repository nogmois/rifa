from django.shortcuts import render, redirect, get_object_or_404
from .forms import SorteioForm, ParticipacaoSorteioForm
from .models import Sorteio, ParticipacaoSorteio
import math
import json



from decimal import Decimal

from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse

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
    
    # Capturar o número do celular na requisição GET
    numero_celular = request.GET.get('verify-number')

    # Filtrar as participações com base no número do celular
    participacoes = ParticipacaoSorteio.objects.filter(sorteio=sorteio, celular_participante=numero_celular)

    # Calcula a hora limite para exclusão (1 hora atrás)
    hora_limite_exclusao = timezone.now() - timedelta(hours=6)
    ParticipacaoSorteio.objects.filter(sorteio=sorteio, data_criacao__lte=hora_limite_exclusao, paga=False).delete()


    # Calcula a hora limite para cada participação
    horas_limites = {}
    for participacao in participacoes:
        hora_limite = participacao.data_criacao + timedelta(hours=72) # 3 dias
        horas_limites[participacao.id] = int(hora_limite.timestamp() * 1000)

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


    # Obter todos os números pagos para este sorteio
    numeros_pagos = set()
    participacoes_pagas = ParticipacaoSorteio.objects.filter(sorteio=sorteio, paga=True)
    for participacao in participacoes_pagas:
        numeros_pagos.update(participacao.numeros_selecionados)

    mostrar_popup_modal = 'verify-number' in request.GET


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        numero_celular = request.GET.get('verify-number')
        numero_cadastrado = ParticipacaoSorteio.objects.filter(celular_participante=numero_celular).exists()
        return JsonResponse({'numero_cadastrado': numero_cadastrado})
    

    # Verificar se tem paga e não paga para colocar a tab no modal
    participacoes_pagas_existem = any(participacao.paga for participacao in participacoes)
    participacoes_nao_pagas_existem = any(not participacao.paga for participacao in participacoes)

    

    if request.method == 'POST':
        form_type = request.POST.get('form_type', '')

        if form_type == 'pagamento':
            # Altera para pago no banco de dados
            numeros_pagos_str = request.POST.get('numeros_pagos', '')
            numeros_pagos = [int(num.strip()) for num in numeros_pagos_str.split(',') if num.strip()]

            
            for num in numeros_pagos:
                ParticipacaoSorteio.objects.filter(sorteio=sorteio, numeros_selecionados__contains=[num]).update(paga=True)
                
            return redirect('detalhe_sorteio', slug=slug)
        
        elif form_type == 'participacao':

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

    quanti_numeros_selecionados =  len(numeros_selecionados) - len(numeros_pagos)

    # Muda o icone quando o modal de pagamento aparece
    participacoes_pagas = [participacao for participacao in participacoes if participacao.paga ]

    # Números selecionados e pagos
    numeros_pago_modal = [participacao.numeros_selecionados for participacao in participacoes if participacao.paga]

    # Números selecionados e não pagos
    numeros_nao_pagos = [participacao.numeros_selecionados for participacao in participacoes if not participacao.paga]

    # Números selecionados e não pagos especifico
    numeros_nao_pagos_por_participacao = {participacao.id: participacao.numeros_selecionados for participacao in participacoes if not participacao.paga}


    print(f'Numero pago - {numeros_pago_modal}')
    print(f'Numeros n pagos - {numeros_nao_pagos}')

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

        'horas_limites': horas_limites,
        'participacoes': participacoes, 

        'numeros_pagos': numeros_pagos, 
        'quanti_numeros_selecionados': quanti_numeros_selecionados,

        'participacoes_pagas': participacoes_pagas,

        'participacoes_pagas_existem': participacoes_pagas_existem,
        'participacoes_nao_pagas_existem': participacoes_nao_pagas_existem,

        'numeros_pago_modal': json.dumps(numeros_pago_modal),
        'numeros_nao_pagos': json.dumps(numeros_nao_pagos), 

        'numeros_nao_pagos_por_participacao': numeros_nao_pagos_por_participacao,  # Mantenha como um dicionário
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

