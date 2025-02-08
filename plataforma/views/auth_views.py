from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Aluno, Professor
from django.contrib.auth.hashers import check_password

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        senha = request.data.get('senha')

        if not email or not senha:
            return Response({'detail': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        user = Aluno.objects.filter(email=email).first() or Professor.objects.filter(email=email).first()

        if not user:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(senha, user.senha):
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        categoria = 'ALUNO' if isinstance(user, Aluno) else 'PROFESSOR'

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
            'categoria': categoria,
            'user_id': user.id,
            'message': f'Login bem-sucedido.'
        }, status=status.HTTP_200_OK)

