from django.db import models
from django.contrib.auth import get_user_model
from enventario.models import ProdutoEstoque

User = get_user_model()

DESTINO_CHOICES = [
    ("SUS", "SUS"),
    ("CONSULTORIO", "Consultório"),
]

class Transacao(models.Model):
    fisioterapeuta = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Fisioterapeuta")
    produto_estoque = models.ForeignKey(ProdutoEstoque, on_delete=models.CASCADE, verbose_name="Produto do Estoque")
    quantidade_retirada = models.PositiveIntegerField(verbose_name="Quantidade retirada")
    destino = models.CharField(max_length=20, choices=DESTINO_CHOICES, verbose_name="Destino")
    data_retirada = models.DateTimeField(auto_now_add=True, verbose_name="Data da retirada")

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        db_table = "transacao"

    def save(self, *args, **kwargs):
        # Diminui a quantidade no estoque ao salvar a transação
        if self.pk is None:
            self.produto_estoque.quantidade -= self.quantidade_retirada
            self.produto_estoque.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fisioterapeuta} retirou {self.quantidade_retirada} de {self.produto_estoque} em {self.data_retirada.strftime('%d/%m/%Y %H:%M')}"
