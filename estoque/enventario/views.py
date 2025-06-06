from django.shortcuts import render, redirect
from .forms import ProdutoForm, ProdutoEstoqueForm, EditarEstoqueForm
from transacao.models import Transacao
from enventario.models import ProdutoEstoque
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from enventario.models import ProdutoEstoque
from django.http import JsonResponse
from .models import Produto
from django.contrib.auth.decorators import login_required

@login_required
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

@login_required
def requisicao(request):
    return render(request, 'enventario/requisicao.html')

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enventario_index')
    else:
        form = ProdutoForm()
    return render(request, 'enventario/cadastrar_produto.html', {'form': form})

@login_required
def produtos_cadastrados(request):
    produtos = Produto.objects.all()
    categorias = Produto._meta.get_field('categoria').choices  # <-- aqui

    return render(request, 'enventario/produtos_cadastrados.html', {
        'produtos': produtos,
        'categorias': categorias,
    })

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    
    if request.method == 'POST':
        produto.nome = request.POST.get('nome')
        produto.categoria = request.POST.get('categoria')
        produto.descricao = request.POST.get('descricao')
        produto.preco = request.POST.get('preco')
        produto.fisioterapia = request.POST.get('fisioterapia') == 'True'
        produto.save()
        return redirect('lista_produtos')  # ajuste esse nome para o nome correto da view da tabela

    return redirect('lista_produtos')

@login_required
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('produtos_cadastrados')
    return render(request, 'enventario/confirmar_exclusao.html', {'produto': produto})


@login_required
def entrada_estoque(request):
    if request.method == 'POST':
        form = ProdutoEstoqueForm(request.POST)
        if form.is_valid():
            novo_estoque = form.save(commit=False)
            produto = novo_estoque.produto

            # Se produto é NÃO PERECÍVEL, atualizar quantidade existente
            if produto.categoria == "NAOPERECIVEL":
                existente = ProdutoEstoque.objects.filter(
                    produto=produto,
                    data_de_validade__isnull=True
                ).first()

                if existente:
                    existente.quantidade += novo_estoque.quantidade
                    existente.save()
                else:
                    novo_estoque.save()
            else:
                # Perecíveis (com validade) devem ter entradas separadas
                novo_estoque.save()

            return redirect('enventario_index')
    else:
        form = ProdutoEstoqueForm()

    return render(request, 'enventario/entrada_estoque.html', {'form': form})

@login_required
def dashboard_fisioterapeuta(request):
    return render(request, 'enventario/dashboard_fisioterapeuta.html')


@login_required
def estoque_atual(request):
    if request.method == 'POST':
        estoque_id = request.POST.get('estoque_id')
        estoque_item = ProdutoEstoque.objects.get(id=estoque_id)
        form = EditarEstoqueForm(request.POST, instance=estoque_item)
        if form.is_valid():
            form.save()
            return redirect('estoque_atual')  # Substitua pelo nome correto da URL
    else:
        estoque = ProdutoEstoque.objects.select_related('produto').all().order_by('produto__nome')
        forms_dict = {item.id: EditarEstoqueForm(instance=item) for item in estoque}
        return render(request, 'enventario/estoque_atual.html', {
            'estoque': estoque,
            'forms_dict': forms_dict,
        })
    

@login_required
@require_POST
def excluir_estoque(request, id):
    item = get_object_or_404(ProdutoEstoque, id=id)
    item.delete()
    return redirect('estoque_atual')  # substitua pelo nome real da sua URL de listagem


@login_required
def categoria_produto_api(request, produto_id):
    produto = Produto.objects.filter(id=produto_id).first()
    if produto:
        return JsonResponse({'categoria': produto.categoria})
    return JsonResponse({'erro': 'Produto não encontrado'}, status=404)

