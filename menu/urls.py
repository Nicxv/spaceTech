from django.urls import path
from django.conf.urls.static import static
from spacetech import settings
from . import views
from django.urls import path
from .views import enviar_publicidad
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from .views import proveedor_list, proveedor_add, proveedor_edit, proveedor_delete

urlpatterns = [
    path('', views.home_view, name='home'),
    path('menu', views.menu, name='menu'),

    path('busqueda_productos/', views.busqueda_productos),
    path('buscar/', views.buscar),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('agregarP', views.agregar_producto, name='agregarP'),
    path('registro', views.registro, name='registro'),
    path('update-profile/', views.update_profile_view, name='update_profile'),

    path('formulario', views.formulario, name='formulario'),
    path('listaU', views.listaU, name='listaU'),
    path('listaP', views.listaP, name='listaP'),
    path('publicidad', enviar_publicidad, name='publicidad'),

    path('listaU/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listaU/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('listaP/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('listaP/modificar/<int:producto_id>/', views.modificarP, name='modificarP'),
    
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),



    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('incrementar_cantidad/<int:item_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('decrementar_cantidad/<int:item_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),


    path('recuperar_contraseña/', auth_views.PasswordResetView.as_view(template_name='recuperar_contraseña.html'), name='password_reset'),
    path('recuperar_contraseña/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('recuperar_contraseña/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('recuperar_contraseña/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('comprar/', views.comprar, name='comprar'),


    


    path('venta_productos/', views.venta_productos, name='venta_productos'),
    path('guardar_direccion/', views.guardar_direccion, name='guardar_direccion'),





    path('proveedores/', proveedor_list, name='proveedor_list'),
    path('proveedor/add/', proveedor_add, name='proveedor_add'),
    path('proveedor/edit/<int:pk>/', proveedor_edit, name='proveedor_edit'),
    path('proveedor/delete/<int:pk>/', proveedor_delete, name='proveedor_delete'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
