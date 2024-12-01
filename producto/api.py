from rest_framework import viewsets, permissions
from .models import Categoria, CategoriaColor, Marca, Usuario, Busqueda,Producto, Talla, Color, NotaIngreso
from .serializers import (
    CategoriaSerializer,
    CategoriaColorSerializer,
    MarcaSerializer,
    UsuarioSerializer,
    BusquedaSerializer,
    ProductoSerializer,
    TallaSerializer,
    ColorSerializer,
    NotaIngresoSerializer
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

# ViewSet para Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductoSerializer

# ViewSet para Talla
class TallaViewSet(viewsets.ModelViewSet):
    queryset = Talla.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TallaSerializer

# ViewSet para Color
class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ColorSerializer

# ViewSet para NotaIngreso
class NotaIngresoViewSet(viewsets.ModelViewSet):
    queryset = NotaIngreso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NotaIngresoSerializer