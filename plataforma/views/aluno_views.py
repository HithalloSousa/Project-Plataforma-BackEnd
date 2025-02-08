from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Aluno
from ..serializers import AlunoSerializer

class AlunoListView(APIView):
    def get(self, request):
        alunos = Aluno.objects.all()
        serializer = AlunoSerializer(alunos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlunoDetailView(APIView):
    def get(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        serializer = AlunoSerializer(aluno)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        serializer = AlunoSerializer(aluno, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        aluno.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlunoCreateView(APIView):
    def post(self, request):
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

