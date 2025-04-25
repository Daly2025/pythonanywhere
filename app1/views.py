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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            email = data.get('email')
            telefono = data.get('telefono')
            direccion = data.get('direccion')
            mensaje = data.get('mensaje')
            carrito = data.get('carrito', [])
            
            mensaje_pedido = "Gracias por tu pedido. Para el pago del mismo haz un bizum al teléfono 655 85 85 85 y en un plazo de 3 a 5 días lo recibirás en tu domicilio.\n\n"
            mensaje_pedido += f"Nombre: {nombre}\n"
            mensaje_pedido += f"Email: {email}\n"
            mensaje_pedido += f"Teléfono: {telefono}\n"
            mensaje_pedido += f"Dirección de envío: {direccion}\n\n"
            
            total = 0
            if carrito:
                for item in carrito:
                    precio = float(item.get('precio', 0))
                    cantidad = int(item.get('cantidad', 0))
                    subtotal = precio * cantidad
                    total += subtotal
                    
                    mensaje_pedido += f"Producto: {item.get('nombre', '')}\n"
                    mensaje_pedido += f"Cantidad: {cantidad}\n"
                    mensaje_pedido += f"Precio unitario: {precio}€\n"
                    mensaje_pedido += f"Subtotal: {subtotal}€\n"
                    mensaje_pedido += "-------------------\n"
                
                mensaje_pedido += f"\nTotal del pedido: {total}€\n"
                mensaje_pedido += "==================\n"
            
            if mensaje:
                mensaje_pedido += f"\nMensaje adicional:\n{mensaje}\n"
            
            mensaje_pedido += "\n\n"
            mensaje_pedido += "Carretera de Verín 22\n"
            mensaje_pedido += "32619 Verín, Ourense\n"
            mensaje_pedido += "Teléfono: 655 85 85 85\n\n"
            mensaje_pedido += """
                 🐝 
    COLMENAR DO CASTELO
         Miel Artesanal
            """
            
            send_mail(
                'Nuevo pedido - Colmenar do Castelo',
                mensaje_pedido,
                'Mieles.Lydia@gmail.com',
                [email, 'Mieles.Lydia@gmail.com'],
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'app1/contacto.html')