# Generated by Django 5.1.3 on 2024-12-06 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotaIngreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotaVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Talla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('categorias', models.ManyToManyField(related_name='colores', to='producto.categoriacolor')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen_url', models.URLField()),
                ('stock', models.PositiveIntegerField(default=0)),
                ('popularidad', models.PositiveIntegerField(default=0)),
                ('fecha_agregado', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.categoria')),
                ('colores', models.ManyToManyField(blank=True, to='producto.color')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='producto.marca')),
                ('tallas', models.ManyToManyField(blank=True, to='producto.talla')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleNotaVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('nota_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='producto.notaventa')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleNotaIngreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('nota_ingreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='producto.notaingreso')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('permisos', models.ManyToManyField(blank=True, related_name='roles', to='producto.permiso')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('password', models.CharField(default='default_password', max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('roles', models.ManyToManyField(blank=True, related_name='usuarios', to='producto.rol')),
            ],
        ),
        migrations.CreateModel(
            name='Busqueda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_busqueda', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.usuario')),
            ],
        ),
    ]
