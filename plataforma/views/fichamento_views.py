from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Fichamento, Aluno
from ..serializers import FichamentoSerializer

class FichamentoCreateView(APIView):
    def post(self, request):
        aluno_id = request.data.get('aluno_id')
        aluno = get_object_or_404(Aluno, id=aluno_id)
        serializer = FichamentoSerializer(data=request.data)
        if serializer.is_valid():
            fichamento = serializer.save()
            aluno.fichamento = fichamento
            aluno.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FichamentoDetailView(APIView):
    def get(self, request, aluno_id, id=None):
        aluno = get_object_or_404(Aluno, id=aluno_id)

        if aluno.fichamento:
            fichamento = aluno.fichamento
            serializer = FichamentoSerializer(fichamento)
            return Response(serializer.data)
        return Response({"detail": "Aluno nao tem fichamento. Crie um novo"})

    def put(self, request, aluno_id ,id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        try:
            fichamento = Fichamento.objects.get(id=id, aluno=aluno)
            serializer = FichamentoSerializer(fichamento, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Fichamento.DoesNotExist:
            return Response({"detail": "Fichamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)