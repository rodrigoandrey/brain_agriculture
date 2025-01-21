from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    total_fazendas = serializers.IntegerField()
    total_hectares = serializers.DecimalField(max_digits=12, decimal_places=2)
    grafico_estado_url = serializers.URLField()
    grafico_cultura_url = serializers.URLField()
    grafico_uso_solo_url = serializers.URLField()
