from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from menu.forms import ArticulosForm, LoginForm, Usuario2Form, UsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.contrib.auth import authenticate, login as auth_login, logout

from menu.models import Articulos, Carrito, CarritoItem, Usuario


# Create your views here.
def home_view(request):
    productos = Articulos.objects.all() 
    return render(request, 'home.html', {'productos': productos})


def busqueda_productos(request):

    return render(request, "busqueda_productos.html")

def buscar(request):
    
    
    if request.GET.get("prd"):

    
        mensaje="Articulo buscado: %r" %request.GET.get("prd")
        producto=request.GET.get("prd")

        #articulos=Articulos.objects.filter(nombre__icontains=producto)

    else:

        mensaje="no has introducido nada"

    

    return HttpResponse(mensaje)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(email=email)
                if user.clave == password:
                    # Crear un objeto User de Django para manejar la autenticación
                    from django.contrib.auth.models import User
                    user_django, created = User.objects.get_or_create(username=user.email, defaults={'email': user.email, 'password': user.clave})
                    auth_login(request, user_django)  # Usamos auth_login para evitar el conflicto de nombres
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('/')  # Redirigir a la página principal
                else:
                    messages.error(request, 'Correo o contraseña incorrectos.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Correo o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    if request.user.is_authenticated:
        try:
            # Obtener el perfil del usuario desde la base de datos
            perfil_usuario = Usuario.objects.get(email=request.user.email)
        except Usuario.DoesNotExist:
            perfil_usuario = None
        
        return render(request, 'profile.html', {'perfil_usuario': perfil_usuario})
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
        return redirect('login')

def detalles(request):
    productos = Articulos.objects.all() 
    return render(request, 'detalles.html', {'productos': productos} )

def registro(request):
    return render(request, 'registro.html')


def publicidad(request):
    return render(request, 'publicidad.html')



#paginas de admin 
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administradores').exists())
def listaU(request):
    usuarios = Usuario.objects.all()  # Recupera todos los usuarios
    return render(request, 'listaU.html', {'usuarios': usuarios})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Administradores').exists())
def listaP(request):
    productos = Articulos.objects.all()  # Recupera todos los usuarios
    return render(request, 'listaP.html', {'productos': productos})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado con éxito')
    return redirect('listaU')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = Usuario2Form(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario modificado con éxito')
            return redirect('listaU')
    else:
        form = Usuario2Form(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos, Comuna, Imagen
from .forms import ArticulosForm, ImagenFormSet

def modificarP(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    if request.method == 'POST':
        form = ArticulosForm(request.POST, request.FILES, instance=producto)
        formset = ImagenFormSet(request.POST, request.FILES, instance=producto)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Producto modificado con éxito')
            return redirect('listaP')
        else:
            print("Formulario no válido:", form.errors, formset.errors)
    else:
        form = ArticulosForm(instance=producto)
        formset = ImagenFormSet(instance=producto)
    return render(request, 'modificarP.html', {'form': form, 'formset': formset, 'producto': producto})
#Plantillas de menu

def menu(request):
    return render(request, 'plantilla/menu.html')

def formulario(request):
    mensaje_exito = None
    mensaje_error = None
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje_exito = "El usuario se registró correctamente."
        else:
            mensaje_error = "Por favor, corrige los errores del formulario."
    else:
        form = UsuarioForm()
    
    return render(request, 'formulario.html', {'form': form, 'mensaje_exito': mensaje_exito, 'mensaje_error': mensaje_error})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos, Imagen
from .forms import ArticulosForm, ImagenFormSet

def agregar_producto(request):
    if request.method == 'POST':
        form = ArticulosForm(request.POST, request.FILES)
        formset = ImagenFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            articulo = form.save()
            for form in formset:
                imagen = form.save(commit=False)
                imagen.articulo = articulo
                imagen.save()
            return redirect('/')
        else:
            print("Formulario no válido:", form.errors, formset.errors)
    else:
        form = ArticulosForm()
        formset = ImagenFormSet()
    return render(request, 'agregarP.html', {'form': form, 'formset': formset})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    imagenes = Imagen.objects.filter(articulo=producto)
    carrito_items_count = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_items_count = CarritoItem.objects.filter(carrito=carrito).count()
    return render(request, 'detalle_producto.html', {'producto': producto, 'imagenes': imagenes, 'carrito_items_count': carrito_items_count})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado con éxito')
    return redirect('listaP')




from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.conf import settings
  # Importa el modelo Fotos

from datetime import datetime, timedelta

def enviar_publicidad(request):
    if request.method == 'POST':
        imagen = request.FILES['imagen']
        tiempo = int(request.POST['tiempo'])  # Convierte el tiempo a entero
        segundos = int(request.POST['segundos'])  # Convierte los segundos a entero
        # Calcula el precio basado en el tiempo y los segundos
        precio = calcular_precio(tiempo, segundos)
        
        # Calcula la fecha de hoy
        fecha_hoy = datetime.now().date()
        # Calcula la fecha de término de la publicidad
        fecha_termino = fecha_hoy + timedelta(weeks=tiempo)

        # Procesa los datos y envía el correo electrónico
        asunto = 'Nueva Publicidad'
        mensaje = f'Se ha recibido una nueva solicitud de publicidad.\n\nPrecio: {precio} CLP\nTiempo: {tiempo} semanas\nSegundos: {segundos}\nFecha de inicio: {fecha_hoy}\nFecha de término: {fecha_termino}'
        email = EmailMessage(asunto, mensaje, settings.EMAIL_HOST_USER, ['alvarover.x@gmail.com'])
        
        # Adjunta la imagen al correo electrónico
        email.attach(imagen.name, imagen.read(), imagen.content_type)
        email.send()

        # Guarda la foto en la base de datos
        
        return redirect('publicidad')
    
    return render(request, 'publicidad.html')

def calcular_precio(tiempo, segundos):
    # Define el precio base en pesos chilenos
    precio_base = 3000
    # Ajusta el precio basado en el tiempo seleccionado
    if tiempo == 2:
        precio_base *= 2  # Duplica el precio para 2 semanas
    elif tiempo == 4:
        precio_base *= 4  # Cuadruplica el precio para 1 mes
    elif tiempo == 12:
        precio_base *= 12  # Multiplica el precio por 12 para 3 meses
    # Ajusta el precio basado en la duración en segundos
    precio_total = precio_base * segundos / 15  # Ajusta el precio en función de la relación 15 segundos = $100
    return precio_total


def update_profile_view(request):
    usuario = Usuario.objects.get(email=request.user.email)
    email_original = request.user.email  # Correo electrónico original del usuario
    if request.method == 'POST':
        form = Usuario2Form(request.POST, instance=usuario)
        if form.is_valid():
            nuevo_email = form.cleaned_data['email']
            if email_original != nuevo_email:
                email_changed = True
                logout(request)  # Cerrar sesión automáticamente si el email cambia
            else:
                email_changed = False
            form.save()
            return redirect('profile')
    else:
        form = Usuario2Form(instance=usuario)
        email_changed = False

    return render(request, 'update_profile.html', {'form': form, 'email_changed': email_changed})



def recuperar_contraseña(request):
    return render(request, 'recuperar_contraseña.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Articulos, Carrito, CarritoItem

@login_required

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        carrito_item.cantidad += 1
    carrito_item.save()

    return redirect('ver_carrito')


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    producto = item.producto

    # Aumentar el stock del producto antes de eliminar el item del carrito
    producto.stock += item.cantidad
    producto.save()

    item.delete()
    return redirect('ver_carrito')


@login_required
def incrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    producto = item.producto

    if producto.stock > item.cantidad:
        item.cantidad += 1
        item.save()
    else:
        messages.error(request, f"No hay suficiente stock para {producto.nombre}")

    return redirect('ver_carrito')

@login_required
def decrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    
    carrito_items = []
    total = 0
    
    for item in items:
        subtotal = item.producto.precio * item.cantidad
        total += subtotal
        carrito_items.append({
            'producto': item.producto,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
            'id': item.id
        })
    
    return render(request, 'ver_carrito.html', {'items': carrito_items, 'total': total})

def my_view(request):
    carrito_items_count = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_items_count = CarritoItem.objects.filter(carrito=carrito).count()
    return render(request, 'mi_template.html', {'carrito_items_count': carrito_items_count})

@login_required
def comprar(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)

    # Verificar stock antes de actualizar
    for item in items:
        producto = item.producto
        if producto.stock < item.cantidad:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}")
            return redirect('ver_carrito')

    # Actualizar stock y vaciar carrito si hay suficiente stock
    for item in items:
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()

    # Vaciar el carrito después de la compra
    items.delete()

    messages.success(request, "Compra realizada con éxito")
    return redirect('ver_carrito')





from django.shortcuts import render
from .models import Carrito, CarritoItem


@login_required
def venta_productos(request):
    if request.user.is_authenticated:
        try:
            # Obtener el perfil del usuario desde la base de datos
            perfil_usuario = Usuario.objects.get(email=request.user.email)
            direccion = perfil_usuario.direccion
        except Usuario.DoesNotExist:
            perfil_usuario = None
            direccion = ""
    else:
        return redirect('login')
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    return render(request, 'venta_productos.html', {'items': items, 'total': total, 'direccion': direccion})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# views.py
@csrf_exempt
@login_required
def guardar_direccion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            direccion = data['direccion']
            usuario = request.user
            perfil_usuario = Usuario.objects.get(email=usuario.email)
            perfil_usuario.direccion = direccion
            perfil_usuario.save()

            # Buscar la comuna en la dirección
            comunas = Comuna.objects.all()
            comuna_nombre = None
            for comuna in comunas:
                if comuna.nombre in direccion:
                    comuna_nombre = comuna.nombre
                    precio_envio = comuna.precio_envio
                    break

            if comuna_nombre is None:
                return JsonResponse({'status': 'error', 'message': 'No Comuna matches the given query.'})

            return JsonResponse({'status': 'success', 'precio_envio': precio_envio})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})
 
    

@csrf_exempt
@login_required
def calcular_precio_envio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            direccion = data['direccion']

            # Extraer la comuna de la dirección
            # Suponemos que la dirección está en el formato "Calle, Comuna, Ciudad, País"
            comuna_nombre = direccion.split(",")[1].strip()
            
            # Buscar la comuna en la base de datos
            comuna = get_object_or_404(Comuna, nombre=comuna_nombre)
            
            # Obtener el precio de envío
            precio_envio = comuna.precio_envio

            return JsonResponse({'status': 'success', 'precio_envio': precio_envio})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})    
    

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Proveedor
from .forms import ProveedorForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor_list.html', {'proveedores': proveedores})

@login_required
@user_passes_test(is_admin)
def proveedor_add(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedor_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedor_confirm_delete.html', {'proveedor': proveedor})


# Clave de google maps api
# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc&callback=initMap&libraries=places" async defer></script>
# AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor
from .forms import ProductosProveedorForm

def agregar_producto_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    if request.method == 'POST':
        form = ProductosProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            producto_proveedor = form.save(commit=False)
            producto_proveedor.proveedor = proveedor
            producto_proveedor.save()
            return redirect('detalle_proveedor', proveedor_id=proveedor.id_proveedor)
    else:
        form = ProductosProveedorForm()
    return render(request, 'agregar_producto_proveedor.html', {'form': form, 'proveedor': proveedor})

def detalle_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    productos = ProductosProveedor.objects.filter(proveedor=proveedor)
    return render(request, 'detalle_proveedor.html', {'proveedor': proveedor, 'productos': productos})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor
from .forms import ProductosProveedorForm

def editar_producto_proveedor(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    if request.method == 'POST':
        form = ProductosProveedorForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle_proveedor', proveedor_id=producto.proveedor.id_proveedor)
    else:
        form = ProductosProveedorForm(instance=producto)
    return render(request, 'editar_producto_proveedor.html', {'form': form, 'producto': producto})

def eliminar_producto_proveedor(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    proveedor_id = producto.proveedor.id_proveedor
    if request.method == 'POST':
        producto.delete()
        return redirect('detalle_proveedor', proveedor_id=proveedor_id)
    return render(request, 'eliminar_producto_proveedor.html', {'producto': producto})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor

def comprar_productos_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    productos = ProductosProveedor.objects.filter(proveedor=proveedor)
    return render(request, 'comprar_productos_proveedor.html', {'proveedor': proveedor, 'productos': productos})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

@login_required
def comprar_producto(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    item, item_created = ProveedorCarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('proveedor_carrito')



from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

@login_required
def proveedor_carrito(request):
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito)
    total = sum(item.producto.precio_costo * item.cantidad for item in items)
    return render(request, 'proveedor_carrito.html', {'carrito': carrito, 'items': items, 'total': total})

@login_required
def agregar_al_proveedor_carrito(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    item, item_created = ProveedorCarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('proveedor_carrito')

@login_required
def eliminar_del_proveedor_carrito(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    item.delete()
    return redirect('proveedor_carrito')

@login_required
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    item.cantidad += 1
    item.save()
    return redirect('proveedor_carrito')

@login_required
def disminuir_cantidad(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect('proveedor_carrito')


from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem
from django.contrib.auth.decorators import login_required

@login_required
def resumen_compra(request):
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito)
    total = sum(item.producto.precio_costo * item.cantidad for item in items)
    return render(request, 'resumen_compra.html', {'items': items, 'total': total})

import os
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from fpdf import FPDF
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProveedorCarritoItem

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resumen de la Compra', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

@login_required
def descargar_pdf(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    proveedor = item.producto.proveedor

    # Crear el PDF
    pdf = PDF()
    pdf.add_page()

    # Añadir contenido al PDF
    pdf.chapter_title("Detalles del Proveedor")
    pdf.chapter_body(f"Nombre de la Empresa: {proveedor.nombre_empresa}")

    pdf.chapter_title("Detalles del Producto")
    pdf.chapter_body(f"Producto: {item.producto.nombre_producto}")
    pdf.chapter_body(f"Precio: ${item.producto.precio_costo}")
    pdf.chapter_body(f"Cantidad: {item.cantidad}")
    pdf.chapter_body(f"Subtotal: ${item.cantidad * item.producto.precio_costo}")

    # Guardar el PDF en un BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resumen_compra_{item_id}.pdf"'
    
    return response


import os
from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
from fpdf import FPDF
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProveedorCarritoItem

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resumen de la Compra', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

@login_required
def aceptar_producto(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    proveedor = item.producto.proveedor

    # Crear el PDF
    pdf = PDF()
    pdf.add_page()

    # Añadir contenido al PDF
    pdf.chapter_title("Detalles del Proveedor")
    pdf.chapter_body(f"Nombre de la Empresa: {proveedor.nombre_empresa}")

    pdf.chapter_title("Detalles del Producto")
    pdf.chapter_body(f"Producto: {item.producto.nombre_producto}")
    pdf.chapter_body(f"Precio: ${item.producto.precio_costo}")
    pdf.chapter_body(f"Cantidad: {item.cantidad}")
    pdf.chapter_body(f"Subtotal: ${item.cantidad * item.producto.precio_costo}")

    # Guardar el PDF en un BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    # Crear el correo electrónico
    email = EmailMessage(
        'Resumen de la Compra',
        'Adjunto encontrará el resumen de la compra.',
        settings.DEFAULT_FROM_EMAIL,
        [proveedor.email_proveedor],
    )
    email.attach(f'resumen_compra_{item_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
    
    # Enviar el correo
    email.send()
    
    # Lógica para aceptar el producto (puede ser guardar en otra tabla, generar una orden, etc.)
    item.delete()  # Aquí solo lo eliminamos del carrito como ejemplo
    
    return redirect('resumen_compra')

@login_required
def rechazar_producto(request, item_id):
    # Lógica de rechazar producto (actualmente vacía)
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    return redirect('resumen_compra')


