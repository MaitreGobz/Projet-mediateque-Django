from django.shortcuts import render

def medias_list(request):
    return render(request, "member/medias_list.html")