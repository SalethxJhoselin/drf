from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .api import CategoriaViewSet, CategoriaColorViewSet, MarcaViewSet, BusquedaViewSet, ProductoViewSet,TallaViewSet,ColorViewSet,NotaIngresoViewSet,NotaVentaViewSet, DetalleNotaVentaViewSet,PermisoViewSet, RolViewSet, UsuarioViewSet

# Crear un router y registrar las rutas
router = DefaultRouter()
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('categorias-colores', CategoriaColorViewSet, basename='categoriacolor')
router.register('marcas', MarcaViewSet, basename='marca')
router.register('busquedas', BusquedaViewSet, basename='busqueda')
router.register('productos', ProductoViewSet, basename='producto')
router.register('tallas', TallaViewSet, basename='talla')
router.register('colores', ColorViewSet, basename='color')
router.register('notas-ingreso', NotaIngresoViewSet, basename='notaingreso')
router.register('notas-venta', NotaVentaViewSet, basename='notaventa')
router.register('detalles-venta', DetalleNotaVentaViewSet, basename='detalleventa')
router.register('permisos', PermisoViewSet, basename='permiso')
router.register('roles', RolViewSet, basename='rol')
router.register('usuarios', UsuarioViewSet, basename='usuario')

# Incluir las rutas en el módulo
urlpatterns = [
    path('', include(router.urls)),  # Incluye todas las rutas generadas automáticamente
    path('recomendaciones/<int:usuario_id>/', views.obtener_recomendaciones, name='obtener_recomendaciones'),               
]
