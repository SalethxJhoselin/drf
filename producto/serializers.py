from rest_framework import serializers
from .models import Categoria, CategoriaColor, Marca, Usuario, Busqueda,NotaIngreso, DetalleNotaIngreso, Producto, Talla, Color,NotaVenta, DetalleNotaVenta,Rol, Permiso, Usuario

# Serializador para Categoría
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# Serializador para Categoría de Color
class CategoriaColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaColor
        fields = '__all__'

# Serializador para Marca
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

# Serializador para Búsqueda
class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields = '__all__'


# Serializador para Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# Serializador para Talla
class TallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = '__all__'

# Serializador para Color
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

# Serializador para DetalleNotaIngreso
class DetalleNotaIngresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaIngreso
        fields = ['producto', 'cantidad']

# Serializador para NotaIngreso
class NotaIngresoSerializer(serializers.ModelSerializer):
    detalles = DetalleNotaIngresoSerializer(many=True)  # Detalles serán una lista

    class Meta:
        model = NotaIngreso
        fields = ['observacion', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')

        # Crear la NotaIngreso
        nota_ingreso = NotaIngreso.objects.create(**validated_data)

        # Crear los Detalles de la NotaIngreso
        for detalle_data in detalles_data:
            DetalleNotaIngreso.objects.create(nota_ingreso=nota_ingreso, **detalle_data)

        return nota_ingreso

# Serializador para Nota de Venta
class NotaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaVenta
        fields = '__all__'

# Serializador para Detalle de Nota de Venta
class DetalleNotaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNotaVenta
        fields = '__all__'

# Serializador para Permiso
class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'

# Serializador para Rol
class RolSerializer(serializers.ModelSerializer):
    permisos = PermisoSerializer(many=True, read_only=True)

    class Meta:
        model = Rol
        fields = '__all__'

# Serializador para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password', 'roles']  # Incluye password
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usuario = super().create(validated_data)
        if password:
            usuario.set_password(password)  # Encripta la contraseña
            usuario.save()
        return usuario