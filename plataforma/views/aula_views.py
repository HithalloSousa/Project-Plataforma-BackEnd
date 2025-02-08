from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Aula, Aluno
from ..serializers import AulaSerializer

class AulaDetailView(APIView):
    def get(self, request, aluno_id, id=None):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        aulas = aluno.aulas.all()
        if aulas.exists():
            serializer = AulaSerializer(aulas, many=True)
            return Response(serializer.data)
        return Response({"detail": "Aluno não tem aulas cadastradas."})

    def put(self, request, aluno_id, id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        try:
            aula = Aula.objects.get(id=id, aluno=aluno)
            serializer = AulaSerializer(aula, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Aula.DoesNotExist:
            return Response({"detail": "Aula não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, aluno_id, id):
        aluno = get_object_or_404(Aluno, id=aluno_id)
        try:
            aula = get_object_or_404(Aula, id=id, alunos__id=aluno_id)
            aula.alunos.remove(aluno)
            if not aula.alunos.exists():
                aula.delete()
            return Response({"detail": "Aula removida com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        except Aula.DoesNotExist:
            return Response({"detail": "Aula não encontrada."}, status=status.HTTP_404_NOT_FOUND)

class AulaCreateView(APIView):
    def post(self, request):
        aluno_id = request.data.get('aluno_id')
        if not aluno_id:
            return Response({"detail": "aluno_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        aluno = get_object_or_404(Aluno, id=aluno_id)
        serializer = AulaSerializer(data=request.data)
        if serializer.is_valid():
            aula = serializer.save()
            aluno.aulas.add(aula)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)