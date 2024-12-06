from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer

class RegistroUsuarioView(APIView):
    def post(self, request):
        data = request.data

        # Validar datos con el serializer
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            usuario = serializer.save()  # Guardar el usuario

            # Generar token JWT
            refresh = RefreshToken.for_user(usuario)
            access_token = str(refresh.access_token)

            # Respuesta con los datos del usuario y token
            return Response({
                'user': serializer.data,
                'access_token': access_token,
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
