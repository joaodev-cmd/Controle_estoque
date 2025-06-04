from django.urls import path
from .views import requisitar_produto, relatorio_retiradas

urlpatterns = [
    path('requisitar/', requisitar_produto, name='requisitar_produto'),
    path('relatorio/', relatorio_retiradas, name='relatorio_retiradas'),
]
