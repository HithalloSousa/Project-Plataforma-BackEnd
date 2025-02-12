from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Material
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..serializers import MaterialSerializer

#View para listar todos os materiais
class MaterialListView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


#View para criar um novo material
class MaterialCreateView(APIView):
    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#View para excluir um material
class MaterialDeleteView(APIView):
    def delete(self, request, pk):
        material = get_object_or_404(Material, pk=pk)
        material.delete()
        return Response({"detail": "Tarefa excluída com sucesso!"}, status=status.HTTP_204_NO_CONTENT)  
    