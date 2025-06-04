from django.urls import path
from .views import index, requisicao, cadastrar_produto, entrada_estoque, dashboard_fisioterapeuta, estoque_atual

urlpatterns = [
    path('', index, name='enventario_index'),
    path('requisicao/', requisicao, name='enventario_requisicao'),
    path('cadastrar-produto/', cadastrar_produto, name='cadastrar_produto'),
    path('entrada-estoque/', entrada_estoque, name='entrada_estoque'),
    path('dashboard-fisioterapeuta/', dashboard_fisioterapeuta, name='dashboard_fisioterapeuta'),
    path('estoque-atual/', estoque_atual, name='estoque_atual'),
]
