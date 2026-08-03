from django.shortcuts import render


def home(request):
    return render(request, "catalog/home.html")


def contacts(request):
    return render(request, "contacts.html")
