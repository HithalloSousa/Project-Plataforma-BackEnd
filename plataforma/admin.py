from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Categoria, NivelAluno, Aluno, Fichamento, Professor, Tarefas, TarefaConcluida, Aula

# Admin para o modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
    ordering = ("nome",)

# Admin para o modelo NivelAluno
@admin.register(NivelAluno)
class NivelAlunoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
    ordering = ("nome",)

# Admin para o modelo Tarefas
@admin.register(Tarefas)
class TarefasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'criadoTime', 'get_alunos', 'arquivo')
    search_fields = ('titulo', 'descricao')
    list_filter = ('criadoTime',)
    ordering = ('-criadoTime',)

    def get_alunos(self, obj):
        return ", ".join([aluno.nome for aluno in obj.alunos.all()])
    get_alunos.short_description = 'Alunos'

# Admin para o modelo Fichamento
@admin.register(Fichamento)
class FichamentoAdmin(admin.ModelAdmin):
    list_display = ('nivel_aluno', 'nivel_detalhado', 'cronograma_conteudos', 'metodologia_personalizada')
    search_fields = ('nivel_detalhado', 'cronograma_conteudos')
    list_filter = ('nivel_aluno',)

# Admin para o modelo Aluno
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'categoria', 'fichamento')
    search_fields = ('nome', 'email', 'categoria__nome')
    list_filter = ('categoria',)
    ordering = ('nome',)

# Admin para o modelo Professor
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'categoria')
    search_fields = ('nome', 'email', 'categoria__nome')
    list_filter = ('categoria',)
    ordering = ('nome',)

    def save_model(self, request, obj, form, change):
        if "senha" in form.changed_data:  # Se a senha foi alterada
            obj.senha = make_password(obj.senha)
        super().save_model(request, obj, form, change)

# Admin para o modelo TarefaConcluida (se aplicável)
@admin.register(TarefaConcluida)
class TarefaConcluidaAdmin(admin.ModelAdmin):
    list_display = ('id','aluno', 'tarefa', 'concluido', 'concluidoTime', 'imagem', 'imagem_correcao')
    search_fields = ('aluno__nome', 'tarefa__titulo')
    list_filter = ('concluido',)
    ordering = ('-concluidoTime',)
    readonly_fields = ('concluidoTime',)


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data', 'get_alunos')
    search_fields = ("titulo",)
    ordering = ("titulo",)

    def get_alunos(self, obj):
        return ", ".join([aluno.nome for aluno in obj.alunos.all()])
    get_alunos.short_description = 'Alunos'  # Define o nome da coluna no admin