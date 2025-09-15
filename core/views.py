from django.shortcuts import render

def home_app(request):
    return render(request, "core/home_app.html")