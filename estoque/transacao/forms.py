from django import forms
from .models import Transacao

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto_estoque', 'quantidade_retirada', 'destino']
        widgets = {
            'produto_estoque': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_retirada': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'destino': forms.Select(attrs={'class': 'form-control'}),
        }
