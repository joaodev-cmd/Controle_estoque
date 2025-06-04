from django.db import models
from core.models import Fornecedor

# Create your models here.
from django.db import models

TIPO_ALIMENTO = [
    ("PERECIVEL", "Perecíveis"),
    ("NAOPERECIVEL", "Não perecíveis"),
]


class Produto(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor")
    categoria = models.CharField(
        verbose_name="Categoria:", max_length=30, choices=TIPO_ALIMENTO)
    nome = models.CharField(verbose_name="Nome do produto:", max_length=194)
    descricao = models.TextField(
        verbose_name="Descrição do produto:", max_length=194, blank=False, null=False)
    preco = models.DecimalField(verbose_name="Preço", max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        db_table = "produto"

    def __str__(self):
        return self.nome


class ProdutoEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name="Quantidade de produto:")
    data_de_validade = models.DateField(verbose_name="Data de validade:", null=True, blank=True)

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
        db_table = "Estoque"

    def __str__(self):
        return self.produto.nome
