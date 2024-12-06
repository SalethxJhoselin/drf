from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils.timezone import now
from datetime import timedelta
from .models import Producto, Busqueda, CategoriaColor
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def obtener_recomendaciones(request, usuario_id):
    # Rango de tiempo para considerar búsquedas recientes (últimos 7 días)
    hace_7_dias = now() - timedelta(days=7)

    # Obtener historial de búsquedas del usuario con relaciones prefetchadas
    busquedas_usuario = Busqueda.objects.filter(usuario=usuario_id).select_related('producto__categoria', 'producto__marca').prefetch_related('producto__colores', 'producto__tallas')

    # Extraer datos relevantes de las búsquedas
    productos_excluidos = {busqueda.producto.id for busqueda in busquedas_usuario}
    estilos = {busqueda.producto.categoria for busqueda in busquedas_usuario}
    marcas = {busqueda.producto.marca for busqueda in busquedas_usuario}
    colores = {color for busqueda in busquedas_usuario for color in busqueda.producto.colores.all()}
    tallas = {talla for busqueda in busquedas_usuario for talla in busqueda.producto.tallas.all()}

    # Obtener categorías de colores relacionadas
    categorias_colores_ids = CategoriaColor.objects.filter(colores__in=colores).values_list('id', flat=True)

    # Consultar productos recientes con anotaciones y prefetch
    productos_recientes = Producto.objects.annotate(
        popularidad_reciente=Count('busqueda', filter=Q(busqueda__fecha_busqueda__gte=hace_7_dias))
    ).select_related('categoria', 'marca').prefetch_related('colores__categorias', 'tallas')

    # Etapa 1: Coincidencia exacta
    recomendaciones_exactas = productos_recientes.filter(
        categoria__in=estilos,
        marca__in=marcas,
        colores__categorias__id__in=categorias_colores_ids,
        tallas__in=tallas,
        stock__gt=0
    ).exclude(id__in=productos_excluidos).distinct().order_by('-popularidad_reciente')

    # Etapa 2: Filtros flexibles
    recomendaciones_flexibles = productos_recientes.filter(
        Q(categoria__in=estilos) |
        Q(colores__categorias__id__in=categorias_colores_ids) |
        Q(tallas__in=tallas),
        stock__gt=0
    ).exclude(id__in=productos_excluidos.union(recomendaciones_exactas.values_list('id', flat=True))).distinct()

    # Ordenar flexibles por relevancia y popularidad
    recomendaciones_flexibles = sorted(
        recomendaciones_flexibles,
        key=lambda p: (
            sum([
                p.categoria in estilos,
                any(c.categorias.filter(id__in=categorias_colores_ids) for c in p.colores.all()),
                any(t in tallas for t in p.tallas.all())
            ]),
            p.popularidad_reciente
        ),
        reverse=True
    )

    # Etapa 3: Productos complementarios
    complementarios = productos_recientes.exclude(
        id__in=productos_excluidos.union(recomendaciones_exactas.values_list('id', flat=True)).union([p.id for p in recomendaciones_flexibles])
    ).filter(stock__gt=0).distinct().order_by('-popularidad_reciente')

    # Construir JSON de respuesta
    recomendaciones = {
        "exactas": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "categoria": p.categoria.nombre,
                "precio": p.precio,
                "imagen": p.imagen_url,
                "stock": p.stock
            }
            for p in recomendaciones_exactas
        ],
        "flexibles": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "categoria": p.categoria.nombre,
                "precio": p.precio,
                "imagen": p.imagen_url,
                "stock": p.stock
            }
            for p in recomendaciones_flexibles
        ],
        "complementarios": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "categoria": p.categoria.nombre,
                "precio": p.precio,
                "imagen": p.imagen_url,
                "stock": p.stock
            }
            for p in complementarios
        ]
    }

    return JsonResponse(recomendaciones)
