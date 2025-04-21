from django.shortcuts import render,HttpResponse

def index(request):
    return render(request, "app1/index.html")
