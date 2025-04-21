from django.shortcuts import render

def home(request):
    return render(request, 'app1/home.html')

def productos(request):
    return render(request, 'app1/productos.html')