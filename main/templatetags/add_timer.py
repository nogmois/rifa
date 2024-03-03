from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='calcular_tempo_restante')
def calcular_tempo_restante(data_criacao):
    prazo_final = data_criacao + timedelta(days=3)  # Exemplo: 3 dias a partir da data de criação
    agora = datetime.now(data_criacao.tzinfo)
    diferenca = prazo_final - agora
    if diferenca.total_seconds() <= 0:
        return "EXPIRADO"
    dias = diferenca.days
    horas, resto = divmod(diferenca.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    return f"{dias}d {horas}h {minutos}m {segundos}s"
