from django.shortcuts import render

# Create your views here.


def handel_not_found(request, exception):
    return render(request, '404.html')
