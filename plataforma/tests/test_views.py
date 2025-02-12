from django.test import TestCase, RequestFactory
from rest_framework import status
from ..models import CategoriaMaterial
from ..views.categoriaMaterial_views import CategoriaMateriaisListView

class CategoriaMaterialListViewTest(TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.factory = RequestFactory()
        self.categoria1 = CategoriaMaterial.objects.create(tipo="Categoria 1")
        self.categoria2 = CategoriaMaterial.objects.create(tipo="Categoria 2")

    def test_get_categorias(self):
        # Cria requisição GET
        request = self.factory.get('/categorias-materiais/')

        # Chama a view
        response = CategoriaMateriaisListView.as_view()(request)

        # Verifica o status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        excepted_data = [
            {'id': self.categoria1.id, 'tipo': 'Categoria 1'},
            {'id': self.categoria2.id, 'tipo': 'Categoria 2'},
        ]
        self.assertEqual(response.data, excepted_data)
