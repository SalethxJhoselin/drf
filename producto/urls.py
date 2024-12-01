from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import CategoriaViewSet, CategoriaColorViewSet, MarcaViewSet, UsuarioViewSet, BusquedaViewSet

# Crear un router y registrar las rutas
router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('categorias-colores', CategoriaColorViewSet, basename='categoriacolor')
router.register('marcas', MarcaViewSet, basename='marca')
router.register('usuarios', UsuarioViewSet, basename='usuario')
router.register('busquedas', BusquedaViewSet, basename='busqueda')

# Incluir las rutas en el módulo
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas generadas automáticamente
]
