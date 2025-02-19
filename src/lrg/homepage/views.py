from django.shortcuts import render, redirect
from django.http import JsonResponse
from homepage.models import Country, City

# Main Pages
def home(request):
    return redirect("posts:search")

def about(request):
    return render(request, 'homepage/about.html')

def contact(request):
    return render(request, 'homepage/contact.html')

# AJAX

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