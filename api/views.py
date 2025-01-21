import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Count, Sum

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboards.seriallizers import DashboardSerializer
from dashboards.utils import generate_pie_chart
from produtores.models import (
    Produtor,
    Fazenda,
    Safra,
    Cultura
)
from produtores.serializers import (
    ProdutorSerializer,
    FazendaSerializer,
    SafraSerializer,
    CulturaSerializer
)

logger_dashboard = logging.getLogger('general')


class ProdutorViewSet(viewsets.ModelViewSet):
    queryset = Produtor.objects.all()
    serializer_class = ProdutorSerializer


class FazendaViewSet(viewsets.ModelViewSet):
    queryset = Fazenda.objects.all()
    serializer_class = FazendaSerializer


class SafraViewSet(viewsets.ModelViewSet):
    queryset = Safra.objects.all()
    serializer_class = SafraSerializer


class CulturaViewSet(viewsets.ModelViewSet):
    queryset = Cultura.objects.all()
    serializer_class = CulturaSerializer


class DashboardView(APIView):
    def get(self, request, *args, **kwargs):  # NOQA
        logger_dashboard.info("Requisição recebida para o dashboard: %s", request.path)
        # Total de fazendas cadastradas
        total_fazendas = Fazenda.objects.count()
        logger_dashboard.info("Total de fazendas cadastradas: %d", total_fazendas)

        # Total de hectares registrados
        total_hectares = Fazenda.objects.aggregate(total_area=Sum('area_total'))['total_area']
        logger_dashboard.info("Total de hectares registrados: %.2f", total_hectares)

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

        logger_dashboard.info("Gráfico de estados salvo como: %s", grafico_estado_path)
        logger_dashboard.info("Gráfico de cultura salvo como: %s", grafico_estado_path)
        logger_dashboard.info("Gráfico de uso solo salvo como: %s", grafico_estado_path)

        # Criar resposta usando o DashboardSerializer
        data = {
            "total_fazendas": total_fazendas,
            "total_hectares": total_hectares,
            "grafico_estado_url": grafico_estado_url,
            "grafico_cultura_url": grafico_cultura_url,
            "grafico_uso_solo_url": grafico_uso_solo_url
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
