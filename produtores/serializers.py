import logging

from rest_framework import serializers

from produtores.models import Produtor, Fazenda, Safra, Cultura

logger_general = logging.getLogger('general')


# CulturaSerializer (Para as culturas associadas a uma safra e fazenda)
class CulturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultura
        fields = ['nome']


# SafraSerializer (Para as safras associadas a uma fazenda, inclui as culturas plantadas)
class SafraSerializer(serializers.ModelSerializer):
    culturas = CulturaSerializer(many=True)

    class Meta:
        model = Safra
        fields = ['nome', 'ano', 'culturas']

    def create(self, validated_data):
        logger_general.info("Criando uma nova Safra: %s", validated_data.get('nome'))
        culturas_data = validated_data.pop('culturas')
        safra = Safra.objects.create(**validated_data)
        logger_general.info("Safra criada com sucesso: %s", validated_data.get('nome'))
        for cultura_data in culturas_data:
            logger_general.info("Criando uma nova Cultura: %s", validated_data.get('nome'))
            Cultura.objects.create(safra=safra, **cultura_data)
            logger_general.info("Cultura criada com sucesso: %s", validated_data.get('nome'))
        return safra


# FazendaSerializer (Para as fazendas associadas ao produtor rural, inclui as safras)
class FazendaSerializer(serializers.ModelSerializer):
    safras = SafraSerializer(many=True)

    class Meta:
        model = Fazenda
        fields = ['nome', 'cidade', 'estado', 'area_total', 'area_agricultavel', 'area_vegetacao', 'safras']

    def validate(self, data):
        """
        Valida as áreas para garantir que a área total seja maior ou igual à soma da área agricultável e vegetação.
        """
        area_total = data.get('area_total')
        area_agricultavel = data.get('area_agricultavel')
        area_vegetacao = data.get('area_vegetacao')

        # Verifica se a soma da área agricultável e da área de vegetação não excede a área total
        if area_total is not None and (area_agricultavel + area_vegetacao > area_total):
            logger_general.info("A soma da área agricultável e da área de "
                                 "vegetação não pode ser maior que a área total.")
            raise serializers.ValidationError(
                {"area_total": [
                    "A soma da área agricultável e da área de vegetação não pode ser maior que a área total."]}
            )

        return data

    def create(self, validated_data):
        logger_general.info("Criando uma nova Fazenda: %s", validated_data.get('nome'))
        safras_data = validated_data.pop('safras')
        fazenda = Fazenda.objects.create(**validated_data)
        logger_general.info("Fazenda criada com sucesso: %s", validated_data.get('nome'))
        for safra_data in safras_data:
            culturas_data = safra_data.pop('culturas')
            logger_general.info("Criando uma nova Safra: %s", validated_data.get('nome'))
            safra = Safra.objects.create(fazenda=fazenda, **safra_data)
            logger_general.info("Safra criada com sucesso: %s", validated_data.get('nome'))
            for cultura_data in culturas_data:
                logger_general.info("Criando uma nova Cultura: %s", validated_data.get('nome'))
                Cultura.objects.create(safra=safra, **cultura_data)
                logger_general.info("Cultura criada com sucesso: %s", validated_data.get('nome'))

        return fazenda


# ProdutorSerializer (Serializer principal para o produtor rural, inclui as fazendas)
class ProdutorSerializer(serializers.ModelSerializer):
    fazendas = FazendaSerializer(many=True)

    class Meta:
        model = Produtor
        fields = ['id', 'cpf', 'cnpj', 'nome', 'fazendas']

    def create(self, validated_data):
        logger_general.info("Criando um novo Produtor: %s", validated_data.get('nome'))
        fazendas_data = validated_data.pop('fazendas')
        produtor = Produtor.objects.create(**validated_data)
        for fazenda_data in fazendas_data:
            safras_data = fazenda_data.pop('safras')
            logger_general.info("Criando uma nova Fazenda: %s", validated_data.get('nome'))
            fazenda = Fazenda.objects.create(produtor=produtor, **fazenda_data)
            logger_general.info("Fazenda criada com sucesso: %s", validated_data.get('nome'))
            for safra_data in safras_data:
                culturas_data = safra_data.pop('culturas')
                logger_general.info("Criando uma nova Fazenda: %s", validated_data.get('nome'))
                safra = Safra.objects.create(fazenda=fazenda, **safra_data)
                logger_general.info("Safra criada com sucesso: %s", validated_data.get('nome'))
                for cultura_data in culturas_data:
                    logger_general.info("Criando uma nova Cultura: %s", validated_data.get('nome'))
                    Cultura.objects.create(safra=safra, fazenda=fazenda, **cultura_data)
                    logger_general.info("Cultura criada com sucesso: %s", validated_data.get('nome'))

        logger_general.info("Produtor criado com sucesso: %s", produtor.nome)
        return produtor
