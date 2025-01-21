from rest_framework.test import APITestCase
from produtores.serializers import ProdutorSerializer, FazendaSerializer, SafraSerializer, CulturaSerializer


class ProdutorSerializerTest(APITestCase):
    def setUp(self):
        self.produtor_data = {
            'cpf': '41203492090',
            'cnpj': '56786086000184',
            'nome': 'João Silva',
            'fazendas': [{
                'nome': 'Fazenda Boa Vista',
                'cidade': 'Cidade A',
                'estado': 'SP',
                'area_total': 1000,
                'area_agricultavel': 800,
                'area_vegetacao': 200,
                'safras': [{
                    'ano': 2021,
                    'culturas': [{
                        'nome': 'Soja'
                    }]
                }]
            }]
        }
        self.produtor_serializer = ProdutorSerializer(data=self.produtor_data)

    def test_produtor_serializer_valid(self):
        # Verifica se o serializer é válido
        self.assertTrue(self.produtor_serializer.is_valid())

    def test_produtor_serializer_invalid(self):
        # Altera a área agricultável para um valor inválido
        self.produtor_data['fazendas'][0]['area_agricultavel'] = 1200
        self.produtor_serializer = ProdutorSerializer(data=self.produtor_data)
        # Verifica se o serializer não é válido devido à validação de área
        self.assertFalse(self.produtor_serializer.is_valid())
        self.assertEqual(str(self.produtor_serializer.errors['fazendas'][0]['area_total'][0]),
                         'A soma da área agricultável e da área de vegetação não pode ser maior que a área total.')

    def test_produtor_serializer_create(self):
        # Testa a criação do produtor e suas fazendas
        self.produtor_serializer.is_valid()
        produtor = self.produtor_serializer.save()
        self.assertEqual(produtor.nome, 'João Silva')
        self.assertEqual(produtor.fazendas.count(), 1)
        self.assertEqual(produtor.fazendas.first().nome, 'Fazenda Boa Vista')


class FazendaSerializerTest(APITestCase):
    def setUp(self):
        self.fazenda_data = {
            'nome': 'Fazenda Boa Vista',
            'cidade': 'Cidade A',
            'estado': 'SP',
            'area_total': 1000,
            'area_agricultavel': 800,
            'area_vegetacao': 200,
            'safras': [{
                'ano': 2021,
                'culturas': [{
                    'nome': 'Soja'
                }]
            }]
        }
        self.fazenda_serializer = FazendaSerializer(data=self.fazenda_data)

    def test_fazenda_serializer_valid(self):
        # Verifica se o serializer é válido
        self.assertTrue(self.fazenda_serializer.is_valid())

    def test_fazenda_serializer_invalid(self):
        # Altera a área agricultável para um valor inválido
        self.fazenda_data['area_agricultavel'] = 1200
        self.fazenda_serializer = FazendaSerializer(data=self.fazenda_data)
        # Verifica se o serializer não é válido devido à validação de área
        self.assertFalse(self.fazenda_serializer.is_valid())
        self.assertEqual(str(self.fazenda_serializer.errors['area_total'][0]),
                         'A soma da área agricultável e da área de vegetação não pode ser maior que a área total.')


class SafraSerializerTest(APITestCase):
    def setUp(self):
        self.safra_data = {
            'ano': 2021,
            'fazenda': 1,
            'culturas': [{'nome': 'Soja'}]
        }
        self.safra_serializer = SafraSerializer(data=self.safra_data)

    def test_safra_serializer_valid(self):
        # Verifica se o serializer é válido
        self.assertTrue(self.safra_serializer.is_valid())

    def test_safra_serializer_invalid(self):
        # Verifica se o serializer é inválido
        self.safra_data['ano'] = False
        self.assertFalse(self.safra_serializer.is_valid())


class CulturaSerializerTest(APITestCase):
    def setUp(self):
        self.cultura_data = {'nome': 'Soja'}
        self.cultura_serializer = CulturaSerializer(data=self.cultura_data)

    def test_cultura_serializer_valid(self):
        # Verifica se o serializer é válido
        self.assertTrue(self.cultura_serializer.is_valid())

    def test_cultura_serializer_invalid(self):
        # Verifica se o serializer é inválido
        self.cultura_data['nome'] = ""
        self.assertFalse(self.cultura_serializer.is_valid())
