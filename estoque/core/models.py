from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do fornecedor")
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    endereco = models.CharField(max_length=200, verbose_name="Endereço", blank=True, null=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        db_table = "fornecedor"

    def __str__(self):
        return self.nome
