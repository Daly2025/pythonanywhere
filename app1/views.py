from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
import json

def home(request):
    return render(request, 'app1/home.html')

def galeria(request):
    return render(request, 'app1/galeria.html')

def productos(request):
    return render(request, 'app1/productos.html')

def contacto_view(request):
    return render(request, 'app1/contacto.html')

def carrito(request):
    return render(request, 'app1/carrito.html')

def enviar_confirmacion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito', [])
            email = data.get('email', '')
            
            # Crear el mensaje del correo
            mensaje = "Gracias por tu pedido. Aquí está el detalle de tu compra:\n\n"
            total = 0
            
            for item in carrito:
                subtotal = float(item['precio']) * int(item['cantidad'])
                mensaje += f"- {item['nombre']}: {item['cantidad']} x {item['precio']}€ = {subtotal}€\n"
                total += subtotal
            
            mensaje += f"\nTotal del pedido: {total}€"
            
            # Enviar el correo
            send_mail(
                'Confirmación de pedido - Colmenar do Castelo',
                mensaje,
                'Mieles.Lydia@gmail.com',  # Actualizado a Gmail
                [email, 'Mieles.Lydia@gmail.com'],  # Añadido CC
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


from django.shortcuts import render, redirect
from django.contrib import messages
import json
import logging

def contacto(request):
    print("DEBUG: Vista contacto() llamada")
    print(f"DEBUG: Método de la petición: {request.method}")
    
    if request.method == 'POST':
        try:
            print("DEBUG: Procesando POST request")
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
            telefono = request.POST.get('telefono')
            mensaje = request.POST.get('mensaje')
            
            print(f"DEBUG: Datos del formulario recibidos:")
            print(f"Nombre: {nombre}")
            print(f"Email: {email}")
            print(f"Teléfono: {telefono}")
            print(f"Mensaje: {mensaje}")
            
            # Obtener el carrito del localStorage
            carrito = request.COOKIES.get('carrito', '[]')
            carrito_items = json.loads(carrito)
            print(f"DEBUG: Carrito recibido: {carrito_items}")
            
            # Crear el mensaje del pedido
            mensaje_pedido = f"Nuevo pedido de {nombre}\n"
            mensaje_pedido += f"Teléfono: {telefono}\n\n"
            mensaje_pedido += "Detalles del pedido:\n"
            total = 0
            
            for item in carrito_items:
                subtotal = float(item['precio']) * int(item['cantidad'])
                mensaje_pedido += f"- {item['nombre']}: {item['cantidad']} x {item['precio']}€ = {subtotal}€\n"
                total += subtotal
            
            mensaje_pedido += f"\nTotal del pedido: {total}€\n"
            mensaje_pedido += f"\nMensaje del cliente:\n{mensaje}"
            
            # Enviar el correo
            try:
                print("DEBUG: Intentando enviar correo...")
                print(f"De: Mieles.Lydia@gmail.com")
                print(f"Para: {email}")
                print(f"Mensaje: {mensaje_pedido}")
                
                from django.conf import settings
                print(f"DEBUG: Configuración de correo:")
                print(f"HOST: {settings.EMAIL_HOST}")
                print(f"PORT: {settings.EMAIL_PORT}")
                print(f"TLS: {settings.EMAIL_USE_TLS}")
                print(f"USER: {settings.EMAIL_HOST_USER}")
                print(f"PASSWORD LENGTH: {len(settings.EMAIL_HOST_PASSWORD)}")
                
                send_mail(
                    'Confirmación de pedido - Colmenar do Castelo',
                    mensaje_pedido,
                    'Mieles.Lydia@gmail.com',
                    [email, 'Mieles.Lydia@gmail.com'],
                    fail_silently=False,
                )
                print("DEBUG: ¡Correo enviado con éxito!")
            except Exception as e:
                import traceback
                print(f"DEBUG: Error al enviar el correo: {str(e)}")
                print(f"DEBUG: Tipo de error: {type(e)}")
                print(f"DEBUG: Traceback completo:")
                print(traceback.format_exc())
                raise  # Re-raise the exception to see it in the response
            
            # Limpiar el carrito después de enviar el correo
            response = redirect('home')
            response.delete_cookie('carrito')
            messages.success(request, '¡Gracias por tu pedido! Te hemos enviado un correo de confirmación.')
            return response
            
        except Exception as e:
            logging.error(f"Error al enviar el correo: {str(e)}")
            messages.error(request, 'Hubo un error al procesar tu pedido. Por favor, inténtalo de nuevo.')
            return render(request, 'app1/contacto.html')
    
    return render(request, 'app1/contacto.html')

# Eliminar las funciones duplicadas contacto() y enviar_confirmacion()