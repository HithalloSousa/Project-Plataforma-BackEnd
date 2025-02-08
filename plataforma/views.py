# # views.py
# from datetime import timezone
# from django.utils.timezone import now
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Categoria, NivelAluno, Tarefas, Fichamento, Aluno, Professor, TarefaConcluida, Aula
# from .serializers import (
#     CategoriaSerializer, NivelAlunoSerializer, TarefasSerializer,
#     FichamentoSerializer, AlunoSerializer, ProfessorSerializer, TarefaConcluidaSerializer,
#     AulaSerializer,
# )
# from django.contrib.auth.hashers import check_password

# #Login Views
# class CustomTokenObtainPairView(TokenObtainPairView):
#     permission_classes = []

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         return response


# class LoginView(APIView):
#     """
#     Custom Login View para autenticação e retorno de token JWT.
#     """
#     permission_classes = []

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         senha = request.data.get('senha')

#         if not email or not senha:
#             return Response({'detail': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Buscar o usuário pelo email nos modelos de Aluno e Professor
#         user = Aluno.objects.filter(email=email).first() or Professor.objects.filter(email=email).first()

#         if not user:
#             return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

#         # Verificar a senha
#         if not check_password(senha, user.senha):
#             return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

#         # Gerar o token JWT
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         # Determinar a categoria do usuário
#         categoria = 'ALUNO' if isinstance(user, Aluno) else 'PROFESSOR'

#         return Response({
#             'access_token': access_token,
#             'refresh_token': str(refresh),
#             'categoria': categoria,
#             'user_id': user.id,
#             'message': f'Login bem-sucedido.'
#         }, status=status.HTTP_200_OK)


# # Aluno Views
# class AlunoListView(APIView):
#     """
#     View para listar todos os alunos.
#     """
#     def get(self, request):
#         alunos = Aluno.objects.all()
#         serializer = AlunoSerializer(alunos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class AlunoDetailView(APIView):
#     """
#     View para visualizar e editar um aluno específico.
#     """
#     def get(self, request, pk):
#         aluno = get_object_or_404(Aluno, pk=pk)
#         serializer = AlunoSerializer(aluno)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         aluno = get_object_or_404(Aluno, pk=pk)
#         serializer = AlunoSerializer(aluno, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         aluno = get_object_or_404(Aluno, pk=pk)
#         aluno.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class AlunoCreateView(APIView):
#     """
#     View para criar um novo aluno.
#     """
#     def post(self, request):
#         serializer = AlunoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #Fichamento Views
# class FichamentoCreateView(APIView):
#     """
#     View para criar um fichamento para um aluno.
#     """
#     def post(self, request):
#         aluno_id = request.data.get('aluno_id')
#         aluno = get_object_or_404(Aluno, id=aluno_id)
#         serializer = FichamentoSerializer(data=request.data)
#         if serializer.is_valid():
#             fichamento = serializer.save()
#             aluno.fichamento = fichamento
#             aluno.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FichamentoDetailView(APIView):
#     def get(self, request, aluno_id, id=None):
#         aluno = get_object_or_404(Aluno, id=aluno_id)

#         if aluno.fichamento:
#             fichamento = aluno.fichamento
#             serializer = FichamentoSerializer(fichamento)
#             return Response(serializer.data)
        
#         return Response({"detail": "Aluno nao tem fichamento. Crie um novo"})

#     def put(self, request, aluno_id ,id):
#         aluno = get_object_or_404(Aluno, id=aluno_id)
#         try:
#             fichamento = Fichamento.objects.get(id=id, aluno=aluno)
#             serializer = FichamentoSerializer(fichamento, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Fichamento.DoesNotExist:
#             return Response({"detail": "Fichamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    

# #Tarefas Views
# class TarefasDetailView(APIView):
#     def get(self, request, aluno_id, id=None):
#         aluno = get_object_or_404(Aluno, id=aluno_id)

#         if aluno.tarefas.exists():  # Verifica se há tarefas associadas
#             tarefas = aluno.tarefas.all()  # Obtém todas as tarefas do aluno
#             serializer = TarefasSerializer(tarefas, many=True)  # Serializa a lista de tarefas
#             return Response(serializer.data)
        
#         # Se o aluno não tem tarefas, retorna uma mensagem
#         return Response({"detail": "Aluno não tem tarefas. Atribua uma tarefa para o aluno."})


# class TarefasListView(APIView):
#     """
#     View para listar todas as tarefas.
#     """
#     def get(self, request):
#         tarefas = Tarefas.objects.all()
#         serializer = TarefasSerializer(tarefas, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class TarefasCreateView(APIView):
#     """
#     View para criar uma tarefa para um aluno.
#     """
#     def post(self, request):
#         print(request.data)
#         serializer = TarefasSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AtribuirTarefaView(APIView):
#     def post(self, request):
#         aluno_id = request.data.get('aluno_id')
#         tarefa_id = request.data.get('tarefa_id')

#         aluno = get_object_or_404(Aluno, id=aluno_id)
#         tarefa = get_object_or_404(Tarefas, id=tarefa_id)

#         tarefa_concluida, created = TarefaConcluida.objects.get_or_create(aluno=aluno, tarefa=tarefa)
        
#         return Response({'detail': 'Tarefa Atribuída com sucesse!!'}, status=status.HTTP_201_CREATED)


# class ConcluirTarefaView(APIView):
#     def post(self, request):
#         aluno_id = request.data.get('aluno_id')
#         tarefa_id = request.data.get('tarefa_id')
#         imagem = request.FILES.get('imagem')
#         imagem_correcao = request.FILES.get('imagem_correcao')

#         try:    
#             aluno = Aluno.objects.get(id=aluno_id)
#             tarefa = Tarefas.objects.get(id=tarefa_id)

#             tarefa_concluida, created = TarefaConcluida.objects.get_or_create(
#                 aluno=aluno, tarefa=tarefa
#             )

#             if imagem:
#                 tarefa_concluida.imagem = imagem
#                 tarefa_concluida.concluido = True
#                 tarefa_concluida.concluidoTime = now()
#                 tarefa_concluida.save()

#             return Response({
#                 "message": "Tarefa concluída com sucesso!",
#                 "imagem_concluida": request.build_absolute_uri(tarefa_concluida.imagem.url) if tarefa_concluida.imagem else None
#             }, status=status.HTTP_200_OK)
        
#         except Aluno.DoesNotExist:
#             return Response({"error": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)
#         except Tarefas.DoesNotExist:
#             return Response({"error": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND)


# class TarefasConcluidasViews(APIView):
#     def get(self, request, aluno_id):
#         try:
#             tarefas_concluidas = TarefaConcluida.objects.filter(aluno_id=aluno_id).select_related('tarefa')
#             resultado = [
#                 {
#                     "id": tarefa.tarefa.id,
#                     "titulo": tarefa.tarefa.titulo,
#                     "descricao": tarefa.tarefa.descricao,
#                     "arquivo": request.build_absolute_uri(tarefa.tarefa.arquivo.url) if tarefa.tarefa.arquivo else None,
#                     "imagem_concluida": request.build_absolute_uri(tarefa.imagem.url) if tarefa.imagem else None,
#                     "imagem_correcao": request.build_absolute_uri(tarefa.imagem_correcao.url) if tarefa.imagem_correcao else None,
#                     "concluido": tarefa.concluido,
#                     "concluidoTime": tarefa.concluidoTime,
#                 }
#                 for tarefa in tarefas_concluidas
#             ]
#             return Response(resultado, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CorrigirTarefaView(APIView):
#     parser_classes = [MultiPartParser, FormParser] 

#     def post(self, request, pk):
#         aluno_id = request.POST.get('aluno_id')
#         # tarefa_id = request.data.get('tarefa_id')
#         imagem_correcao = request.FILES.get('imagem_correcao')

#         if not (aluno_id and imagem_correcao):
#             return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

#         # Busca a tarefa concluída do aluno
#         tarefa_concluida = get_object_or_404(TarefaConcluida, aluno_id=aluno_id, tarefa_id=pk)

#         # Atualiza a imagem de correção
#         tarefa_concluida.imagem_correcao = imagem_correcao
#         tarefa_concluida.save()

#         return Response({"message": "Correção enviada com sucesso!"}, status=status.HTTP_200_OK)


# class ExcluirTarefaView(APIView):
#     def delete(self, request, pk):
#         tarefa = get_object_or_404(Tarefas, pk=pk)
#         tarefa.delete()
#         return Response({"detail": "Tarefa excluída com sucesso!"}, status=status.HTTP_204_NO_CONTENT)    


# class RemoverAlunoDaTarefaView(APIView):
#     def patch(self, request, tarefa_id):
#         aluno_id = request.data.get("aluno_id")
#         aluno = get_object_or_404(Aluno, pk=aluno_id)
#         tarefa = get_object_or_404(Tarefas, pk=tarefa_id)
        
#         # Remove aluno da tarefa
#         if aluno in tarefa.alunos.all():
#             tarefa.alunos.remove(aluno)
#             serializer = TarefasSerializer(tarefa)  # Serializa a tarefa atualizada
#             return Response({
#                 "detail": "Aluno removido da tarefa com sucesso!",
#                 "tarefa": serializer.data  # Retorna os dados atualizados da tarefa
#             }, status=status.HTTP_200_OK)
        
#         return Response({"detail": "Aluno não encontrado nesta tarefa."}, status=status.HTTP_400_BAD_REQUEST)
    

# #Niveis Views
# class NiveisListView(APIView):
#     def get(self, request):
#         niveis = NivelAluno.objects.all()
#         serializer = NivelAlunoSerializer(niveis, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)   


# class AulaDetailView(APIView):
#     def get(self, request, aluno_id, id=None):
#         print(aluno_id)
#         aluno = get_object_or_404(Aluno, id=aluno_id)

#         # Verifica se o aluno tem aulas
#         aulas = aluno.aulas.all()  # Usando related_name 'aulas'
#         if aulas.exists():
#             serializer = AulaSerializer(aulas, many=True)
#             return Response(serializer.data)
#         return Response({"detail": "Aluno não tem aulas cadastradas."})

#     def put(self, request, aluno_id, id):
#         aluno = get_object_or_404(Aluno, id=aluno_id)
#         try:
#             aula = Aula.objects.get(id=id, aluno=aluno)  # Certifique-se de que o campo no modelo seja 'aluno'
#             serializer = AulaSerializer(aula, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Aula.DoesNotExist:  # Corrigido para Aula.DoesNotExist
#             return Response({"detail": "Aula não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
#     def delete(self, request, aluno_id, id):
#         aluno = get_object_or_404(Aluno, id=aluno_id)

#         try:
#             aula = get_object_or_404(Aula, id=id, alunos__id=aluno_id)  # Correção no filtro
#             aula.alunos.remove(aluno)  # Remove apenas o aluno dessa aula

#             # Se a aula não estiver associada a nenhum aluno após a remoção, pode ser deletada
#             if not aula.alunos.exists():
#                 aula.delete()

#             return Response({"detail": "Aula removida com sucesso."}, status=status.HTTP_204_NO_CONTENT)
#         except Aula.DoesNotExist:
#             return Response({"detail": "Aula não encontrada."}, status=status.HTTP_404_NOT_FOUND)


# class AulaCreateView(APIView):
#     def post(self, request):
#         aluno_id = request.data.get('aluno_id')
#         if not aluno_id:
#             return Response({"detail": "aluno_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

#         aluno = get_object_or_404(Aluno, id=aluno_id)
#         serializer = AulaSerializer(data=request.data)
#         if serializer.is_valid():
#             aula = serializer.save()
#             aluno.aulas.add(aula)  # Adiciona a aula ao aluno (para ManyToManyField)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)