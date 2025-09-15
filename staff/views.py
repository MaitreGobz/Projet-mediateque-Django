from django.shortcuts import render

def home_staff(request):
    return render(request, "staff/home_staff.html")