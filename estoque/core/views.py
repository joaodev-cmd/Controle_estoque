from django.shortcuts import get_object_or_404, render, redirect
from .forms import FornecedorForm
from .models import Fornecedor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_fornecedor')
    else:
        form = FornecedorForm()
    return render(request, 'core/cadastrar_fornecedor.html', {'form': form})

@login_required
def fornecedores_cadastrados(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'core/fornecedores_cadastrados.html', {'fornecedores': fornecedores})

@login_required
@csrf_exempt
def editar_fornecedor_ajax(request, id):
    if request.method == 'POST':
        fornecedor = get_object_or_404(Fornecedor, id=id)
        data = json.loads(request.body)

        fornecedor.nome = data.get('nome')
        fornecedor.telefone = data.get('telefone')
        fornecedor.email = data.get('email')
        fornecedor.endereco = data.get('endereco')
        fornecedor.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def deletar_fornecedor_ajax(request, id):
    if request.method == 'POST':
        fornecedor = get_object_or_404(Fornecedor, id=id)
        fornecedor.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
