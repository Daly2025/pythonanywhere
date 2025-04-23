from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto_view, name='contacto'),
    path('carrito/', views.carrito, name='carrito'),
    path('galeria/', views.galeria, name='galeria'),
]