from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Busqueda, Producto

@receiver(post_save, sender=Busqueda)
def actualizar_popularidad(sender, instance, created, **kwargs):
    if created:  # Solo cuando se crea una nueva búsqueda
        producto = instance.producto
        producto.popularidad += 1  # Incrementar la popularidad
        producto.save()
