from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from cloudinary.models import CloudinaryField

# Create your models here.

# Modelo de Categoria
class Categoria(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    nome = models.CharField(max_length=100, choices=[('ALUNO', 'Aluno'), ('PROFESSOR', 'Professor')])

    def __str__(self) -> str:
        return f'{self.nome}'


# Modelo Nível dos Alunos
class NivelAluno(models.Model):
    class Meta:
        verbose_name = 'Nível do Inglês'
        verbose_name_plural = 'Níveis do Inglês'

    nome = models.CharField(
    max_length=100,
    choices=[
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]
    )   
    
    def __str__(self):
        return self.nome


# Modelo de Tarefas
class Tarefas(models.Model):
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    arquivo = models.FileField(upload_to='documentos/', null=True, blank=True)
    criadoTime = models.DateTimeField(auto_now_add=True)
    alunos = models.ManyToManyField('Aluno', through='TarefaConcluida', related_name='tarefas_associadas', related_query_name='tarefa')

    def __str__(self):
        return self.titulo


class TarefaConcluida(models.Model):
    """
    Modelo intermediário para armazenar o status de conclusão de uma tarefa por um aluno.
    """
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)  # Relação com o aluno
    tarefa = models.ForeignKey('Tarefas', on_delete=models.CASCADE)  # Relação com a tarefa
    imagem = CloudinaryField('tarefas/', null=True, blank=True)
    concluido = models.BooleanField(default=False)  # Status de conclusão
    concluidoTime = models.DateTimeField(null=True, blank=True)  # Data de conclusão
    imagem_correcao = CloudinaryField('tarefas/correcoes/', null=True, blank=True)

    class Meta:
        unique_together = ('aluno', 'tarefa')  # Garante que cada aluno só pode ter uma entrada por tarefa

    def __str__(self):
        return f'{self.aluno.nome} - {self.tarefa.titulo} - Concluído: {self.concluido}'


class Aula(models.Model):
    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'

    titulo = models.CharField(max_length=200)
    data = models.DateField()

    def __str__(self):
        return self.titulo


# Modelo de Fichamento
class Fichamento(models.Model):
    nivel_aluno = models.ForeignKey(NivelAluno, on_delete=models.SET_NULL, blank=True, null=True)
    nivel_detalhado = models.TextField()
    cronograma_conteudos = models.TextField()
    metodologia_personalizada = models.TextField()

    def __str__(self):
        return self.nivel_detalhado


# Modelo da Pessoa
class Pessoa(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome
    
    def set_password(self, raw_password):
        self.senha = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)


class Aluno(Pessoa):
    fichamento = models.OneToOneField(Fichamento, on_delete=models.SET_NULL, null=True, blank=True)
    tarefas = models.ManyToManyField('Tarefas', through='TarefaConcluida', related_name='alunos_associados', related_query_name='aluno')
    aulas = models.ManyToManyField(Aula, related_name='alunos')

    def __str__(self):
        return f'Aluno: {self.nome}'


class Professor(Pessoa):
    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return f'Professor: {self.nome}'
    