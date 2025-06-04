from django.urls import path
from .views import cadastrar_fornecedor

urlpatterns = [
    path('cadastrar-fornecedor/', cadastrar_fornecedor, name='cadastrar_fornecedor'),
]
