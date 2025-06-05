from django.urls import path
from .views import cadastrar_fornecedor,editar_fornecedor_ajax,deletar_fornecedor_ajax, fornecedores_cadastrados

urlpatterns = [
    path('cadastrar-fornecedor/', cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('fornecedores/', fornecedores_cadastrados, name='fornecedores_cadastrados'),
    path('fornecedor/<int:id>/editar/ajax/', editar_fornecedor_ajax, name='editar_fornecedor_ajax'),
    path('fornecedor/<int:id>/deletar/ajax/', deletar_fornecedor_ajax, name='deletar_fornecedor_ajax'),


]
