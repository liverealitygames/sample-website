from django.shortcuts import render
from django.template import RequestContext
from django.http import JsonResponse
from community.const import GAME_FORMATS
from homepage.models import Location, Country, City, Region

def home(request):
    return render(request, 'homepage/index.html', context={
        "countries": list(Country.objects.values("id", "name")),
        "binary_filters": [
            ("Filmed only", "filmed"),
        ]
    })

def login(request):
    return render(request, 'homepage/login.html')

def register(request):
    return render(request, 'homepage/register.html')

def get_cities(request):
    country_id = request.GET.get("country_id")
    cities = list(str(city) for city in City.objects.filter(country_id=country_id))
    return JsonResponse({"cities": cities})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request, exception):
    return render(request, '500.html', status=500)

handler404 = custom_404
handler500 = custom_500