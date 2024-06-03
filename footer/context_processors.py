from .models import Information


def information(request):
    info = Information.objects.filter(id=1).first()
    return {'info': info}
