
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render

from dashboards.utils import generate_pie_chart
from produtores.models import (
    Fazenda,
    Cultura
)


def teste(request):
    if request.method == 'GET':
        # Total de fazendas cadastradas
        total_fazendas = Fazenda.objects.count()

        # Total de hectares registrados
        total_hectares = Fazenda.objects.aggregate(total_area=Sum('area_total'))['total_area']

        # Gerar gráficos
        estados = Fazenda.objects.values('estado').annotate(total=Count('estado'))
        estados_list = [estado['estado'] for estado in estados]
        total_estados = [estado['total'] for estado in estados]
        estado_chart_buf = generate_pie_chart(total_estados, estados_list, "Distribuição de Fazendas por Estado")

        culturas = Cultura.objects.values('nome').annotate(total=Count('nome'))
        culturas_list = [cultura['nome'] for cultura in culturas]
        total_culturas = [cultura['total'] for cultura in culturas]
        cultura_chart_buf = generate_pie_chart(total_culturas, culturas_list, "Distribuição de Culturas Plantadas")

        areas = Fazenda.objects.aggregate(
            area_agricultavel_total=Sum('area_agricultavel'),
            area_vegetacao_total=Sum('area_vegetacao')
        )
        labels_uso_solo = ['Área Agricultável', 'Área de Vegetação']
        values_uso_solo = [areas['area_agricultavel_total'], areas['area_vegetacao_total']]
        uso_solo_chart_buf = generate_pie_chart(values_uso_solo, labels_uso_solo,
                                                     "Uso do Solo (Agricultável vs Vegetação)")

        # Caminho para salvar os gráficos, com nomes fixos
        grafico_estado_path = 'grafico_estado.png'
        grafico_cultura_path = 'grafico_cultura.png'
        grafico_uso_solo_path = 'grafico_uso_solo.png'

        # Excluir arquivos antigos, se existirem
        if default_storage.exists(grafico_estado_path):
            default_storage.delete(grafico_estado_path)
        if default_storage.exists(grafico_cultura_path):
            default_storage.delete(grafico_cultura_path)
        if default_storage.exists(grafico_uso_solo_path):
            default_storage.delete(grafico_uso_solo_path)

        # Salvar os gráficos com o nome fixo
        default_storage.save(grafico_estado_path, ContentFile(estado_chart_buf.getvalue()))
        default_storage.save(grafico_cultura_path, ContentFile(cultura_chart_buf.getvalue()))
        default_storage.save(grafico_uso_solo_path, ContentFile(uso_solo_chart_buf.getvalue()))

        # Criar URLs para os gráficos
        base_url = settings.BASE_URL
        grafico_estado_url = f"{base_url}/{grafico_estado_path}"
        grafico_cultura_url = f"{base_url}/{grafico_cultura_path}"
        grafico_uso_solo_url = f"{base_url}/{grafico_uso_solo_path}"

        # Criar resposta usando o DashboardSerializer
        context = {
            "total_fazendas": total_fazendas,
            "total_hectares": total_hectares,
            "grafico_estado_url": grafico_estado_url,
            "grafico_cultura_url": grafico_cultura_url,
            "grafico_uso_solo_url": grafico_uso_solo_url
        }

        return render(request, 'dashboards/dashboard.html', context)
    else:
        return HttpResponse(status=503)
