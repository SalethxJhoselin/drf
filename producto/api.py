from rest_framework import viewsets, permissions
from .models import Categoria, CategoriaColor, Marca, Usuario, Busqueda,Producto, Talla, Color, NotaIngreso,NotaVenta, DetalleNotaVenta,Rol, Permiso, Usuario
from .serializers import (
    CategoriaSerializer,
    CategoriaColorSerializer,
    MarcaSerializer,
    UsuarioSerializer,
    BusquedaSerializer,
    ProductoSerializer,
    TallaSerializer,
    ColorSerializer,
    NotaIngresoSerializer,
    NotaVentaSerializer, 
    DetalleNotaVentaSerializer,
    RolSerializer, 
    PermisoSerializer 
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

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

# ViewSet para Nota de Venta
class NotaVentaViewSet(viewsets.ModelViewSet):
    queryset = NotaVenta.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = NotaVentaSerializer

# ViewSet para Detalle de Nota de Venta
class DetalleNotaVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleNotaVenta.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DetalleNotaVentaSerializer

# ViewSet para Permiso
class PermisoViewSet(viewsets.ModelViewSet):
    queryset = Permiso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PermisoSerializer

# ViewSet para Rol
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def asignar_permisos(self, request, pk=None):
        try:
            rol = self.get_object()  # Obtiene el rol según el ID en la URL
            permisos_ids = request.data.get('permisos', [])
            permisos = Permiso.objects.filter(id__in=permisos_ids)

            # Asignar permisos al rol
            rol.permisos.set(permisos)
            rol.save()

            return Response({'message': 'Permisos asignados con éxito'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UsuarioSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def asignar_rol(self, request, pk=None):
        usuario = self.get_object()
        rol_id = request.data.get('rol_id')

        try:
            rol = Rol.objects.get(id=rol_id)
            usuario.roles.add(rol)
            return Response({"message": "Rol asignado con éxito."}, status=status.HTTP_200_OK)
        except Rol.DoesNotExist:
            return Response({"error": "El rol no existe."}, status=status.HTTP_400_BAD_REQUEST)