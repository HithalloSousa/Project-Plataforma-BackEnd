from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import CategoriaMaterial
from ..serializers import CategoriaMaterialSerializer

class CategoriaMateriaisListView(APIView):
    def get(self, request):
        categorias = CategoriaMaterial.objects.all()
        serializer = CategoriaMaterialSerializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
