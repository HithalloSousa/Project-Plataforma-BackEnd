from django.urls import path
from .views import (CustomTokenObtainPairView, LoginView, AlunoListView, AlunoDetailView, 
                    AlunoCreateView, FichamentoCreateView, NiveisListView, FichamentoDetailView, 
                    TarefasListView,TarefasCreateView, TarefasDetailView, AtribuirTarefaView, ConcluirTarefaView, CorrigirTarefaView,
                    ExcluirTarefaView, RemoverAlunoDaTarefaView, TarefasConcluidasViews, AulaDetailView, AulaCreateView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'),
    ##Aluno
    path('alunos/', AlunoListView.as_view(), name='aluno_list'),  # Para ver todos os alunos
    path('aluno/<int:pk>/', AlunoDetailView.as_view(), name='aluno_detail'), # Para ver e editar um aluno específico
    path('criar-alunos/', AlunoCreateView.as_view(), name='aluno-create'),
    #Fichamento
    path('criar-fichamento/', FichamentoCreateView.as_view(), name='fichamento-create'),
    path('fichamento/<int:aluno_id>/', FichamentoDetailView.as_view(), name='fichamento-detail'),
    path('fichamento/<int:aluno_id>/<int:id>/', FichamentoDetailView.as_view(), name='fichamento-detail2'),
    #Agenda Aulas
    path('criar-aulas/', AulaCreateView.as_view(), name='agenda-create'),
    path('aulas/<int:aluno_id>/', AulaDetailView.as_view(), name='agenda-detail'),
    #Nivel de inglês
    path('nivels/', NiveisListView.as_view(), name='niveis list'),
    #Tarefas Professor
    path('tarefas/', TarefasListView.as_view(), name='tarefas_list'),  # Para ver todos as tarefas
    path('criar-tarefas/', TarefasCreateView.as_view(), name='tarefas_create'), # Para criar tarefas
    path('tarefas/<int:aluno_id>/', TarefasConcluidasViews.as_view(), name='fichamento-detail'),
    path('atribuir-tarefa/', AtribuirTarefaView.as_view(), name='atribuir-tarefa'),
    path('deletar/tarefa/<int:pk>/', ExcluirTarefaView.as_view(), name='excluir_tarefa'),
    path("remover-aluno/<int:tarefa_id>/", RemoverAlunoDaTarefaView.as_view(), name="remover-aluno"),
    path('corrigir-tarefa/<int:pk>/', CorrigirTarefaView.as_view(), name='corrigir-tarefa'),
    #Tarefas Aluno
    path('tarefas/concluir-tarefa/', ConcluirTarefaView.as_view(), name='concluir-tarefa'),
] 