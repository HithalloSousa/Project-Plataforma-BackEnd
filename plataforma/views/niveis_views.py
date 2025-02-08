from ..serializers import NivelAlunoSerializer
from ..models import NivelAluno
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class NiveisListView(APIView):
    def get(self, request):
        niveis = NivelAluno.objects.all()
        serializer = NivelAlunoSerializer(niveis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 