from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils.timezone import now
from datetime import timedelta
from .models import Producto, Busqueda, CategoriaColor

def obtener_recomendaciones(request, usuario_id):
    # Rango de tiempo para considerar búsquedas recientes (últimos 7 días)
    hace_7_dias = now() - timedelta(days=7)

    # Obtener historial de búsquedas del usuario
    busquedas_usuario = Busqueda.objects.filter(usuario=usuario_id)
    productos_excluidos = [busqueda.producto.id for busqueda in busquedas_usuario]

    # Extraer atributos más buscados
    estilos = [busqueda.producto.categoria for busqueda in busquedas_usuario]
    marcas = [busqueda.producto.marca for busqueda in busquedas_usuario]
    colores = [color for busqueda in busquedas_usuario for color in busqueda.producto.colores.all()]
    tallas = [talla for busqueda in busquedas_usuario for talla in busqueda.producto.tallas.all()]

    # Obtener categorías de colores relacionadas
    categorias_colores = CategoriaColor.objects.filter(colores__in=colores).distinct()

    # Calcular popularidad reciente
    productos_recientes = Producto.objects.annotate(
        popularidad_reciente=Count(
            'busqueda', filter=Q(busqueda__fecha_busqueda__gte=hace_7_dias)
        )
    )

    # Etapa 1: Coincidencia exacta
    recomendaciones_exactas = productos_recientes.filter(
        categoria__in=estilos,
        marca__in=marcas,
        colores__categorias__in=categorias_colores,
        tallas__in=tallas,
        stock__gt=0
    ).exclude(id__in=productos_excluidos).distinct().order_by('-popularidad_reciente')

    # Etapa 2: Filtros flexibles
    recomendaciones_flexibles = productos_recientes.filter(
        Q(categoria__in=estilos) |
        Q(colores__categorias__in=categorias_colores) |
        Q(tallas__in=tallas),
        stock__gt=0
    ).exclude(id__in=productos_excluidos + list(recomendaciones_exactas.values_list('id', flat=True))).distinct()

    recomendaciones_flexibles = sorted(
        recomendaciones_flexibles,
        key=lambda p: (
            sum([p.categoria in estilos,
                 any(c.categorias.filter(id__in=categorias_colores.values_list('id', flat=True)) for c in p.colores.all()),
                 any(t in tallas for t in p.tallas.all())
            ]),
            p.popularidad_reciente
        ),
        reverse=True
    )

    # Etapa 3: Productos complementarios
    complementarios = productos_recientes.exclude(
        id__in=productos_excluidos + list(recomendaciones_exactas.values_list('id', flat=True)) +
        [p.id for p in recomendaciones_flexibles]
    ).filter(stock__gt=0).distinct().order_by('-popularidad_reciente')

    # Construir JSON de respuesta
    recomendaciones = {
        "exactas": [
            {"nombre": p.nombre, "categoria": p.categoria.nombre, "precio": p.precio, "popularidad": p.popularidad_reciente}
            for p in recomendaciones_exactas
        ],
        "flexibles": [
            {"nombre": p.nombre, "categoria": p.categoria.nombre, "precio": p.precio, "popularidad": p.popularidad_reciente}
            for p in recomendaciones_flexibles
        ],
        "complementarios": [
            {"nombre": p.nombre, "categoria": p.categoria.nombre, "precio": p.precio, "popularidad": p.popularidad_reciente}
            for p in complementarios
        ]
    }

    return JsonResponse(recomendaciones)
