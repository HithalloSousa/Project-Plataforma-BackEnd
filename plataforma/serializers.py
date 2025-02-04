from rest_framework import serializers
from .models import Categoria, NivelAluno, TarefaConcluida, Tarefas, Fichamento, Aluno, Professor, Aula


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']


class NivelAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelAluno
        fields = ['id', 'nome']


class TarefaConcluidaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)  # Nome do aluno
    concluido = serializers.BooleanField()
    data_conclusao = serializers.DateTimeField()

    class Meta:
        model = TarefaConcluida
        fields = ['id', 'imagem', 'concluido', 'concluidoTime', 'imagem_correcao']


class FichamentoSerializer(serializers.ModelSerializer):
    nivel_aluno = serializers.PrimaryKeyRelatedField(queryset=NivelAluno.objects.all())

    class Meta:
        model = Fichamento
        fields = ['id', 'nivel_aluno', 'nivel_detalhado', 'cronograma_conteudos', 'metodologia_personalizada']


class AlunoSerializer(serializers.ModelSerializer):
    fichamento = FichamentoSerializer(write_only=True, required=False)
    tarefas = TarefaConcluidaSerializer(many=True, read_only=True, source='tarefa_set')
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.filter(nome='ALUNO'),
        source='categoria',
        write_only=True
    )
    tarefas_concluidas = TarefaConcluidaSerializer(
        many=True,
        read_only=True,
        source='tarefa_concluida_set'
    )

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'email', 'telefone', 'categoria_id', 'tarefas' ,'tarefas_concluidas', 'fichamento', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        # Remove a senha dos dados validados
        senha = validated_data.pop('senha')
        
        # Remove o fichamento dos dados validados (se existir)
        fichamento_data = validated_data.pop('fichamento', None)
        
        # Cria o aluno
        aluno = Aluno(**validated_data)
        
        # Define a senha criptografada
        aluno.set_password(senha)
        
        # Cria o fichamento (se os dados forem fornecidos)
        if fichamento_data:
            fichamento_serializer = FichamentoSerializer(data=fichamento_data)
            if fichamento_serializer.is_valid():
                fichamento = fichamento_serializer.save()
                aluno.fichamento = fichamento
        
        # Salva o aluno no banco de dados
        aluno.save()
        return aluno

    def update(self, instance, validated_data):
        # Atualiza a senha (se fornecida)
        if 'senha' in validated_data:
            senha = validated_data.pop('senha')
            instance.set_password(senha)
        
        # Atualiza os demais campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Salva as alterações
        instance.save()
        return instance


class TarefasSerializer(serializers.ModelSerializer):
    alunos = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), many=True)
    tarefa_concluida = serializers.SerializerMethodField()
    
    class Meta:
        model = Tarefas
        fields = ['id', 'titulo', 'descricao', 'criadoTime', 'alunos', 'arquivo', 'tarefa_concluida']

    def get_tarefa_concluida(self, obj):
        request = self.context.get('request')

        # Se `request` não existe, retorna None para evitar erro
        if not request:
            return None

        aluno_id = request.query_params.get('aluno_id')

        # Se `aluno_id` não for fornecido, retorna None
        if not aluno_id:
            return None

        # Busca a tarefa concluída para o aluno específico
        tarefa_concluida = TarefaConcluida.objects.filter(tarefa=obj, aluno_id=aluno_id).first()

        # Retorna os dados da tarefa concluída ou None se não existir
        return TarefaConcluidaSerializer(tarefa_concluida).data if tarefa_concluida else None


class ProfessorSerializer(serializers.ModelSerializer):
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.filter(nome='PROFESSOR'),
        source='categoria',
        write_only=True
    )

    class Meta:
        model = Professor
        fields = ['id', 'nome', 'email', 'telefone', 'categoria_id', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        professor = Professor(**validated_data)
        professor.set_password(senha)
        professor.save()
        return professor


class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = ['id', 'titulo', 'data']
