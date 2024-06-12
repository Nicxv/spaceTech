import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Usuario(models.Model):
    
    nombre_usuario = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    tfno = models.CharField(max_length=8, verbose_name="Telefono")
    clave = models.CharField(max_length=30)
    confirmar_clave = models.CharField(max_length=30)
    direccion = models.CharField(max_length=255, verbose_name="Dirección", null=True, blank=True)
    def __str__(self):
         return '  %s  %s ' %(self.nombre, self.apellido)

    

class Articulos(models.Model):
    
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    foto = models.ImageField(upload_to='static/img/', blank=True, null=True)
    marca = models.CharField(max_length=30, default='Sin Marca')
    precio_oferta = models.IntegerField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Pedidos(models.Model):
        numero=models.IntegerField()
        fecha=models.DateField()
        entregado=models.BooleanField()


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    agregado_en = models.DateTimeField(default=timezone.now)        
    




class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    precio_envio = models.IntegerField(default=1)  # Precio de envío en pesos chilenos

    def __str__(self):
        return self.nombre




class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_boleta = models.CharField(max_length=30)
    fecha = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Venta {self.id} - Usuario {self.usuario.nombre_usuario}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Venta {self.venta.id} - Articulo {self.articulo.nombre}'








class Imagen(models.Model):
    articulo = models.ForeignKey(Articulos, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='static/img/')

    def __str__(self):
        return f"Imagen de {self.articulo.nombre}"
class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True, editable=False)
    rut_empresa = models.CharField(max_length=13, verbose_name='RUT de la Empresa')
    nombre_empresa = models.CharField(max_length=100, verbose_name='Nombre de la Empresa')
    representante_legal = models.CharField(max_length=100, verbose_name='Representante Legal', default="")
    contacto_empresa = models.CharField(max_length=50, verbose_name='Contacto de la Empresa')
    direccion_proveedor = models.CharField(max_length=255, verbose_name='Dirección', default="sin direccion")
    email_proveedor = models.EmailField(max_length=70, unique=True, null=True, blank=True)

    def str(self):
        return self.nombre_empresa
    

class Compra(models.Model):
    id_orden_compra = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.RESTRICT)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class DetalleCompra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_orden_compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='detalles')
    correlativo = models.IntegerField(editable=False)
    id_articulo = models.ForeignKey('Articulos', verbose_name='Articulos', on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de Costo')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sub Total')

    class Meta:
        unique_together = ('id_orden_compra', 'correlativo')

    def save(self, args, **kwargs):
        if not self.correlativo:
            last_correlativo = DetalleCompra.objects.filter(id_orden_compra=self.id_orden_compra).count()
            self.correlativo = last_correlativo + 1
        super().save(args, **kwargs)