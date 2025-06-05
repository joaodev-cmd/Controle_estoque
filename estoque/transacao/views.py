from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransacaoForm
from .models import Transacao

@login_required
def requisitar_produto(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST, user=request.user)  # ← ESSENCIAL
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.fisioterapeuta = request.user
            transacao.save()
            return redirect('dashboard_fisioterapeuta')
    else:
        form = TransacaoForm(user=request.user)  # ← ESSENCIAL
    return render(request, 'transacao/requisitar_produto.html', {'form': form})




@login_required
def relatorio_retiradas(request):
    relatorios = Transacao.objects.select_related('fisioterapeuta', 'produto_estoque__produto').order_by('-data_retirada')
    return render(request, 'transacao/relatorio_retiradas.html', {'relatorios': relatorios})
