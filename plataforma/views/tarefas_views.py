from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ..models import Tarefas, Aluno, TarefaConcluida
from rest_framework.parsers import MultiPartParser, FormParser
from ..serializers import TarefasSerializer
from datetime import timezone
from django.utils.timezone import now

class TarefasDetailView(APIView):
    def get(self, request, aluno_id, id=None):
        aluno = get_object_or_404(Aluno, id=aluno_id)

        if aluno.tarefas.exists():
            tarefas = aluno.tarefas.all()
            serializer = TarefasSerializer(tarefas, many=True)
            return Response(serializer.data)
        return Response({"detail": "Aluno não tem tarefas. Atribua uma tarefa para o aluno."})


class TarefasListView(APIView):
    def get(self, request):
        tarefas = Tarefas.objects.all()
        serializer = TarefasSerializer(tarefas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TarefasCreateView(APIView):
    def post(self, request):
        serializer = TarefasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtribuirTarefaView(APIView):
    def post(self, request):
        aluno_id = request.data.get('aluno_id')
        tarefa_id = request.data.get('tarefa_id')

        aluno = get_object_or_404(Aluno, id=aluno_id)
        tarefa = get_object_or_404(Tarefas, id=tarefa_id)

        tarefa_concluida, created = TarefaConcluida.objects.get_or_create(aluno=aluno, tarefa=tarefa)
        return Response({'detail': 'Tarefa Atribuída com sucesse!!'}, status=status.HTTP_201_CREATED)


class ConcluirTarefaView(APIView):
    def post(self, request):
        aluno_id = request.data.get('aluno_id')
        tarefa_id = request.data.get('tarefa_id')
        imagem = request.FILES.get('imagem')
        imagem_correcao = request.FILES.get('imagem_correcao')

        try:    
            aluno = Aluno.objects.get(id=aluno_id)
            tarefa = Tarefas.objects.get(id=tarefa_id)

            tarefa_concluida, created = TarefaConcluida.objects.get_or_create(
                aluno=aluno, tarefa=tarefa
            )

            if imagem:
                tarefa_concluida.imagem = imagem
                tarefa_concluida.concluido = True
                tarefa_concluida.concluidoTime = now()
                tarefa_concluida.save()

            return Response({
                "message": "Tarefa concluída com sucesso!",
                "imagem_concluida": request.build_absolute_uri(tarefa_concluida.imagem.url) if tarefa_concluida.imagem else None
            }, status=status.HTTP_200_OK)
        except Aluno.DoesNotExist:
            return Response({"error": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Tarefas.DoesNotExist:
            return Response({"error": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND)


class TarefasConcluidasViews(APIView):
    def get(self, request, aluno_id):
        try:
            tarefas_concluidas = TarefaConcluida.objects.filter(aluno_id=aluno_id).select_related('tarefa')
            resultado = [
                {
                    "id": tarefa.tarefa.id,
                    "titulo": tarefa.tarefa.titulo,
                    "descricao": tarefa.tarefa.descricao,
                    "arquivo": request.build_absolute_uri(tarefa.tarefa.arquivo.url) if tarefa.tarefa.arquivo else None,
                    "imagem_concluida": request.build_absolute_uri(tarefa.imagem.url) if tarefa.imagem else None,
                    "imagem_correcao": request.build_absolute_uri(tarefa.imagem_correcao.url) if tarefa.imagem_correcao else None,
                    "concluido": tarefa.concluido,
                    "concluidoTime": tarefa.concluidoTime,
                }
                for tarefa in tarefas_concluidas
            ]
            return Response(resultado, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CorrigirTarefaView(APIView):
    parser_classes = [MultiPartParser, FormParser] 

    def post(self, request, pk):
        aluno_id = request.POST.get('aluno_id')
        imagem_correcao = request.FILES.get('imagem_correcao')

        if not (aluno_id and imagem_correcao):
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        tarefa_concluida = get_object_or_404(TarefaConcluida, aluno_id=aluno_id, tarefa_id=pk)
        tarefa_concluida.imagem_correcao = imagem_correcao
        tarefa_concluida.save()

        return Response({"message": "Correção enviada com sucesso!"}, status=status.HTTP_200_OK)

class ExcluirTarefaView(APIView):
    def delete(self, request, pk):
        tarefa = get_object_or_404(Tarefas, pk=pk)
        tarefa.delete()
        return Response({"detail": "Tarefa excluída com sucesso!"}, status=status.HTTP_204_NO_CONTENT)    

class RemoverAlunoDaTarefaView(APIView):
    def patch(self, request, tarefa_id):
        aluno_id = request.data.get("aluno_id")
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        tarefa = get_object_or_404(Tarefas, pk=tarefa_id)
        
        if aluno in tarefa.alunos.all():
            tarefa.alunos.remove(aluno)
            serializer = TarefasSerializer(tarefa)
            return Response({
                "detail": "Aluno removido da tarefa com sucesso!",
                "tarefa": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Aluno não encontrado nesta tarefa."}, status=status.HTTP_400_BAD_REQUEST)