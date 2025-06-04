from django.shortcuts import render, redirect
from .forms import FornecedorForm

# Create your views here.

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_fornecedor')
    else:
        form = FornecedorForm()
    return render(request, 'core/cadastrar_fornecedor.html', {'form': form})
