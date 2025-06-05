from django.urls import path
from .views import index, requisicao, cadastrar_produto, entrada_estoque, dashboard_fisioterapeuta, estoque_atual, excluir_estoque, categoria_produto_api,produtos_cadastrados, editar_produto, deletar_produto

urlpatterns = [
    path('', index, name='enventario_index'),
    path('requisicao/', requisicao, name='enventario_requisicao'),
    path('cadastrar-produto/', cadastrar_produto, name='cadastrar_produto'),
    path('entrada-estoque/', entrada_estoque, name='entrada_estoque'),
    path('dashboard-fisioterapeuta/', dashboard_fisioterapeuta, name='dashboard_fisioterapeuta'),
    path('estoque-atual/', estoque_atual, name='estoque_atual'),
    path('estoque/excluir/<int:id>/', excluir_estoque, name='excluir_estoque'),
    path('api/produto/<int:produto_id>/categoria/', categoria_produto_api, name='categoria_produto_api'),
    path('produtos/', produtos_cadastrados, name='produtos_cadastrados'),
    path('produtos/editar/<int:id>/', editar_produto, name='editar_produto'),
    path('produtos/deletar/<int:id>/', deletar_produto, name='deletar_produto'),

]
