from django.db import models
from django.utils.text import slugify

class Sorteio(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='imagens_sorteios/')
    slug = models.SlugField(unique=True, blank=True)

    numero = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super(Sorteio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome
