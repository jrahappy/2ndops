from django.shortcuts import render


def home(request):
    return render(request, "dashboard/_base.html")


def about(request):
    return render(request, "dashboard/_base.html")
