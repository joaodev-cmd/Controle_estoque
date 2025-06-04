from django.shortcuts import render, redirect
from .forms import ProdutoForm, ProdutoEstoqueForm
from transacao.models import Transacao
from enventario.models import ProdutoEstoque
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def index(request):
    # Fisioterapeuta com maior gasto por produto
    gastos_por_fisio = list(
        Transacao.objects.values('fisioterapeuta__username', 'produto_estoque__produto__nome')
        .annotate(total_gasto=Sum(F('quantidade_retirada') * F('produto_estoque__produto__preco')))
        .order_by('-total_gasto')
    )
    for g in gastos_por_fisio:
        if g['total_gasto'] is not None:
            g['total_gasto'] = float(g['total_gasto'])

    # Produtos com mais saídas
    produtos_mais_saidas = list(
        Transacao.objects.values('produto_estoque__produto__nome')
        .annotate(total_saida=Sum('quantidade_retirada'))
        .order_by('-total_saida')[:5]
    )
    for p in produtos_mais_saidas:
        if p['total_saida'] is not None:
            p['total_saida'] = int(p['total_saida'])

    # Gastos totais por fisioterapeuta
    gastos_fisioterapeuta = list(
        Transacao.objects.values('fisioterapeuta__username')
        .annotate(total_gasto=Sum(F('quantidade_retirada') * F('produto_estoque__produto__preco')))
        .order_by('-total_gasto')
    )
    for g in gastos_fisioterapeuta:
        if g['total_gasto'] is not None:
            g['total_gasto'] = float(g['total_gasto'])

    # Distribuição de retiradas por destino
    destino_data = list(
        Transacao.objects.values('destino')
        .annotate(total=Sum('quantidade_retirada'))
    )
    for d in destino_data:
        if d['total'] is not None:
            d['total'] = int(d['total'])

    return render(request, 'enventario/index.html', {
        'gastos_por_fisio': gastos_por_fisio,
        'produtos_mais_saidas': produtos_mais_saidas,
        'gastos_fisioterapeuta': gastos_fisioterapeuta,
        'destino_data': destino_data,
    })

def requisicao(request):
    return render(request, 'enventario/requisicao.html')

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enventario_index')
    else:
        form = ProdutoForm()
    return render(request, 'enventario/cadastrar_produto.html', {'form': form})

def entrada_estoque(request):
    if request.method == 'POST':
        form = ProdutoEstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enventario_index')
    else:
        form = ProdutoEstoqueForm()
    return render(request, 'enventario/entrada_estoque.html', {'form': form})

def dashboard_fisioterapeuta(request):
    return render(request, 'enventario/dashboard_fisioterapeuta.html')

def estoque_atual(request):
    estoque = ProdutoEstoque.objects.select_related('produto').all().order_by('produto__nome')
    return render(request, 'enventario/estoque_atual.html', {'estoque': estoque})
