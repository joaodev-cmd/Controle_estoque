from django import forms
from transacao.models import Transacao
from enventario.models import ProdutoEstoque

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto_estoque', 'quantidade_retirada', 'destino']
        widgets = {
            'produto_estoque': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_retirada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        base_qs = ProdutoEstoque.objects.filter(quantidade__gt=0)

        if user and user.groups.filter(name='fisioterapeuta').exists():
            base_qs = base_qs.filter(produto__fisioterapia=True)

        self.fields['produto_estoque'].queryset = base_qs

    def clean(self):
        cleaned_data = super().clean()
        produto_estoque = cleaned_data.get('produto_estoque')
        quantidade_retirada = cleaned_data.get('quantidade_retirada')

        if produto_estoque and quantidade_retirada:
            if quantidade_retirada > produto_estoque.quantidade:
                self.add_error('quantidade_retirada', f"Quantidade indisponível. Estoque atual: {produto_estoque.quantidade}")
