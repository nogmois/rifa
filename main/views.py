from django.shortcuts import render, redirect, get_object_or_404
from .forms import SorteioForm, ParticipacaoSorteioForm
from .models import Sorteio, ParticipacaoSorteio
import math
import json
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.http import require_http_methods
from decimal import Decimal

from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse, HttpResponseBadRequest

from django.views.decorators.http import require_POST

from .utils import send_sms_via_textbelt, format_number_for_sms

def home(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'index.html', {'sorteios': sorteios})



def sorteio(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'sorteios/sorteios.html', {'sorteios': sorteios})



def detalhe_sorteio(request, slug):
    sorteio = get_object_or_404(Sorteio, slug=slug)
    form = ParticipacaoSorteioForm()
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

            print(numeros_pagos_str) 
            numeros_pagos = [int(num.strip()) for num in numeros_pagos_str.split(',') if num.strip()]
        
            # Enviar SMS após o pagamento
            celular_participante = request.POST.get('celular_participante')
            if celular_participante:
                celular_participante_formatado = format_number_for_sms(celular_participante)
                mensagem_pagamento = "Obrigado por efetuar o pagamento."
                #send_sms_via_textbelt(celular_participante_formatado, mensagem_pagamento)
            
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

                # Enviar SMS após a participação
                celular_participante = participacao.celular_participante
                nome_participante = participacao.nome_participante
                mensagem_participacao = f"Parabéns, {nome_participante}, por escolher seus números. Acesse o site para efetuar o pagamento."
                celular_participante_formatado = format_number_for_sms(celular_participante)
                #send_sms_via_textbelt(celular_participante_formatado, mensagem_participacao)


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



def adm(request, slug=None):
    sorteio = None
    if slug:
        # Acessando um sorteio existente para atualizar
        sorteio = get_object_or_404(Sorteio, slug=slug)
        if request.method == 'POST':
            # Atualizar o sorteio existente
            form = SorteioForm(request.POST, request.FILES, instance=sorteio)
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                print("Erros do formulário na atualização:", form.errors)
        else:
            # Abrir formulário com dados do sorteio para edição
            form = SorteioForm(instance=sorteio)
    else:
        # Criar um novo sorteio
        if request.method == 'POST':
            form = SorteioForm(request.POST, request.FILES)
            if form.is_valid():
                novo_sorteio = form.save(commit=False)

                # Obter e processar o valor do preço
                preco_str = request.POST.get('preco', '')
                preco_str = preco_str.replace('R$ ', '').replace(',', '.')
                preco_decimal = Decimal(preco_str)
                novo_sorteio.preco = preco_decimal

                novo_sorteio.save()
                return redirect('home')
            else:
                print("Erros do formulário na criação:", form.errors)
        else:
            form = SorteioForm()

    participacoes = ParticipacaoSorteio.objects.filter(paga=False)
    sorteios = Sorteio.objects.all() 
    return render(request, 'admin/adm.html', {'form': form, 'sorteios': sorteios, 'sorteio': sorteio, 'participacoes': participacoes})



@require_POST  # Garante que esta view só possa ser acessada via POST
def excluir_sorteio(request, slug):
    sorteio = get_object_or_404(Sorteio, slug=slug)
    sorteio.delete()
    return redirect('adm')


def calcular_tempo_restante(data_criacao):
    prazo_final = data_criacao + timedelta(days=3)  # 3 dias a partir da data de criação
    agora = datetime.now(data_criacao.tzinfo)  # Certifique-se de usar o mesmo fuso horário
    diferenca = prazo_final - agora
    if diferenca.total_seconds() <= 0:
        return "EXPIRADO"
    dias, resto = divmod(diferenca.seconds, 86400)
    horas, resto = divmod(resto, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{dias}d {horas}h {minutos}m {segundos}s"

def participantes_json(request):
    participacoes = ParticipacaoSorteio.objects.filter(paga=False)
    dados = [
        {
            'id': participacao.id,
            'nome_participante': participacao.nome_participante,
            'sorteio': {
                'nome': participacao.sorteio.nome,
                'slug': participacao.sorteio.slug
            },
            'tempo_restante': calcular_tempo_restante(participacao.data_criacao)
        }
        for participacao in participacoes
    ]
    return JsonResponse(dados, safe=False)


@require_http_methods(["POST"])
def alterar_horas(request, participacao_id):
    try:
        body = json.loads(request.body)
        horas = int(body.get('horas'))
        participacao = ParticipacaoSorteio.objects.get(id=participacao_id)

        nova_data_criacao = participacao.data_criacao + timedelta(hours=horas)
        if nova_data_criacao < timezone.now():
            return JsonResponse({"status": "erro", "mensagem": "Não é possível definir uma hora no passado"})

        participacao.data_criacao = nova_data_criacao
        participacao.save()
        return JsonResponse({"status": "sucesso", "mensagem": "Horas atualizadas"})

    except ParticipacaoSorteio.DoesNotExist:
        return HttpResponseBadRequest("Participação não encontrada")
    except (ValueError, KeyError):
        return HttpResponseBadRequest("Dados inválidos")
