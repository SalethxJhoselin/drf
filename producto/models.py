from django.db import models
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Manager para Usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)  # Encripta la contraseña
        usuario.save(using=self._db)
        return usuario


# Modelo personalizado para Usuario
class Usuario(AbstractBaseUser):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField('Rol', related_name='usuarios', blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email


# Modelo Rol
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    permisos = models.ManyToManyField('Permiso', related_name='roles', blank=True)

    def __str__(self):
        return self.nombre


# Modelo Permiso
class Permiso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# Señal para normalizar el nombre de las categorías
@receiver(pre_save, sender=Categoria)
def normalize_categoria_name(sender, instance, **kwargs):
    instance.nombre = instance.nombre.lower().capitalize()


# Modelo CategoriaColor (categorías de colores)
class CategoriaColor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ejemplo: "Cálido", "Frío", etc.

    def __str__(self):
        return self.nombre


# Señal para normalizar el nombre de las categorías de colores
@receiver(pre_save, sender=CategoriaColor)
def normalize_categoria_color_name(sender, instance, **kwargs):
    instance.nombre = instance.nombre.lower().capitalize()


# Modelo Color
class Color(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ejemplo: "Rojo", "Azul", etc.
    categorias = models.ManyToManyField(CategoriaColor, related_name="colores")

    def __str__(self):
        return self.nombre


# Señal para normalizar el nombre de los colores
@receiver(pre_save, sender=Color)
def normalize_color_name(sender, instance, **kwargs):
    instance.nombre = instance.nombre.lower().capitalize()


# Modelo Talla
class Talla(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Ejemplo: "M", "L", etc.

    def __str__(self):
        return self.nombre


# Señal para normalizar el nombre de las tallas
@receiver(pre_save, sender=Talla)
def normalize_talla_name(sender, instance, **kwargs):
    instance.nombre = instance.nombre.upper()  # Convertir todo a mayúsculas


# Modelo Marca
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# Señal para normalizar el nombre de las marcas
@receiver(pre_save, sender=Marca)
def normalize_marca_name(sender, instance, **kwargs):
    instance.nombre = instance.nombre.lower().capitalize()


# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField()
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    colores = models.ManyToManyField(Color, blank=True)
    tallas = models.ManyToManyField(Talla, blank=True)
    stock = models.PositiveIntegerField(default=0)
    popularidad = models.PositiveIntegerField(default=0)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"


# Modelo Busqueda
class Busqueda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_busqueda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} buscó {self.producto.nombre} el {self.fecha_busqueda}"

# Modelo Nota de Ingreso
class NotaIngreso(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Nota de Ingreso #{self.id} - {self.fecha}"

# Modelo DetalleNotaIngreso
class DetalleNotaIngreso(models.Model):
    nota_ingreso = models.ForeignKey(NotaIngreso, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# Señal para actualizar el stock del producto al registrar una Nota de Ingreso
@receiver(post_save, sender=DetalleNotaIngreso)
def actualizar_stock(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save()

# Modelo Nota de Venta
class NotaVenta(models.Model):
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de Venta #{self.id} - {self.fecha}"


# Modelo Detalle de Nota de Venta
class DetalleNotaVenta(models.Model):
    nota_venta = models.ForeignKey(NotaVenta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

    def clean(self):
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock para el producto '{self.producto.nombre}'.")

# Señal para descontar stock después de guardar un DetalleNotaVenta
@receiver(post_save, sender=DetalleNotaVenta)
def descontar_stock(sender, instance, **kwargs):
    producto = instance.producto
    if producto.stock < instance.cantidad:
        raise ValidationError(f"No hay suficiente stock para el producto '{producto.nombre}'.")
    producto.stock -= instance.cantidad
    producto.save()

