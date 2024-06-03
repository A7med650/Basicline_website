from django.shortcuts import render
from .models import Service, Aboutus

# Create your views here.


def service(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'services.html', context)


def about_us(request):
    cards = Aboutus.objects.all()
    context = {
        'cards': cards,
    }
    return render(request, 'about.html', context)
