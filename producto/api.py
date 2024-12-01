from rest_framework import viewsets, permissions
from .models import Categoria, CategoriaColor, Marca, Usuario, Busqueda
from .serializers import (
    CategoriaSerializer,
    CategoriaColorSerializer,
    MarcaSerializer,
    UsuarioSerializer,
    BusquedaSerializer
)

# ViewSet para Categoría
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer

# ViewSet para Categoría de Color
class CategoriaColorViewSet(viewsets.ModelViewSet):
    queryset = CategoriaColor.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaColorSerializer

# ViewSet para Marca
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = MarcaSerializer

# ViewSet para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsuarioSerializer

# ViewSet para Búsqueda
class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BusquedaSerializer
