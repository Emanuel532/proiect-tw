from django.http import JsonResponse
def index(request):
    mesaj_test_django = "SALUT!"

    data = {
        'mesaj_django' : mesaj_test_django
    }

    return JsonResponse(data)
