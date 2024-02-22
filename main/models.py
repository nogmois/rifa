from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

class Sorteio(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='imagens_sorteios/')
    slug = models.SlugField(unique=True, blank=True)

    numero = models.IntegerField()

    participacoes = models.ManyToManyField('ParticipacaoSorteio', related_name='sorteios')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super(Sorteio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ParticipacaoSorteio(models.Model):
    sorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE)
    nome_participante = models.CharField(max_length=200)
    celular_participante = models.CharField(max_length=20, unique=True)
    numeros_selecionados = ArrayField(models.IntegerField())

    def __str__(self):
        return f"Participação de {self.nome_participante} no sorteio {self.sorteio.nome}"

