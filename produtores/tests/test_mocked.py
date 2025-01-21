from django.urls import reverse
from rest_framework.test import APITestCase
from factories import ProdutorFactory, FazendaFactory, SafraFactory, CulturaFactory
from produtores.models import Produtor, Fazenda, Cultura


class MockedDataTests(APITestCase):
    def setUp(self):
        # Cria 10 produtores, cada um com 1 a 3 fazendas e 1 a 2 culturas por fazenda
        for _ in range(10):
            produtor = ProdutorFactory()
            fazendas = FazendaFactory.create_batch(3, produtor=produtor)
            for fazenda in fazendas:
                safras = SafraFactory.create_batch(3, fazenda=fazenda)
                for safra in safras:
                    CulturaFactory.create_batch(3, fazenda=fazenda, safra=safra)

    def test_produtores_e_fazendas_mockadas(self):
        # Testa se os produtores e fazendas foram criados corretamente
        self.assertEqual(Produtor.objects.count(), 10)
        self.assertTrue(Fazenda.objects.count() > 0)
        self.assertTrue(Cultura.objects.count() > 0)

    def test_dashboard_com_dados_mockados(self):
        # Testa o dashboard com os dados mockados
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Verifica que os dados agregados estão presentes
        self.assertIn('total_fazendas', data)
        self.assertIn('total_hectares', data)
        self.assertIn('grafico_estado_url', data)
        self.assertIn('grafico_uso_solo_url', data)
        self.assertIn('grafico_cultura_url', data)
