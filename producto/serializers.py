from rest_framework import serializers
from .models import Categoria, CategoriaColor, Marca, Usuario, Busqueda

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

# Serializador para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

# Serializador para Búsqueda
class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields = '__all__'
