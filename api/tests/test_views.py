from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from produtores.models import Produtor, Fazenda, Safra, Cultura


class DashboardViewTest(APITestCase):
    def setUp(self):
        # Criar alguns dados para o dashboard
        produtor = Produtor.objects.create(cpf='12345678901', nome='João Silva')
        fazenda = Fazenda.objects.create(
            nome='Fazenda Boa Vista', cidade='Cidade A', estado='SP',
            area_total=1000, area_agricultavel=800, area_vegetacao=200,
            produtor=produtor
        )
        safra = Safra.objects.create(nome='Safra 2021', ano=2021, fazenda=fazenda)
        Cultura.objects.create(nome='Soja', safra=safra, fazenda=fazenda)

    def test_dashboard_view(self):
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIn('total_fazendas', data)
        self.assertIn('total_hectares', data)
        self.assertIn('grafico_estado_url', data)
        self.assertIn('grafico_cultura_url', data)
        self.assertIn('grafico_uso_solo_url', data)

    def test_dashboard_graphs(self):
        # Teste se os gráficos são gerados e os URLs de download estão no retorno
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertIn('grafico_estado_url', response.data)
        self.assertIn('grafico_cultura_url', response.data)
        self.assertIn('grafico_uso_solo_url', response.data)
