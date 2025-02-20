from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.http import JsonResponse

from community.const import GAME_FORMATS
from posts.models import Post
from community.models import Season
from homepage.models import Location
from posts.const import COUNTRIES

def browse(request):
    posts = Post.objects.filter(season__status="Casting")
    return render(request, "posts/browse.html", context={
        "posts":posts,
        "posts_per_page":12,
        })

@login_required
def create(request):
    if request.method == "POST":
        description = request.POST.get("description", None)
        season = get_object_or_404(Season, id=request.POST.get("seasonId"))
        Post.objects.create(
            season=season,
            description=description,
        )
    return render(request, "posts/create.html", context={
        "game_formats":GAME_FORMATS,
        "seasons":Season.objects.filter(community__owner=request.user.profile)
        })

def info(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "posts/info.html", context={"post":post})

def search(request):
    if request.method == "POST":
        country_short = request.POST.get("countrySelected", None)
        city = request.POST.get("citySelected", None)

        locations = Location.objects.all()

        if country_short:
            locations = Location.objects.filter(country_short=country_short)
        if city:
            city = city.split(",")[0]
            locations = locations.filter(city=city)

        game_format = request.POST.get("gameFormat", None)

        query = request.POST.get("query", None)
        posts = Post.objects.all()

        if game_format:
            posts = posts.filter(season__format=game_format)

        if query:
            posts = posts.annotate(
                search=SearchVector("description","season__name","season__format"),
            ).filter(search=query)

        if country_short or city:
            posts = posts.filter(season__location__in=locations)


        return render(request, 'posts/search.html', context={
            "countries": COUNTRIES.items(),
            "formats": GAME_FORMATS,
            "binary_filters": [
                ("Filmed only", "filmed"),
            ],
            "posts":posts,
            "info":[country_short, city, str(locations), query],
        })

    return render(request, 'posts/search.html', context={
        "countries": COUNTRIES.items(),
        "formats": GAME_FORMATS,
        "binary_filters": [
            ("Filmed only", "filmed"),
        ]
    })

# AJAX

def get_cities(request):
    country_id = request.GET.get("country_id")
    cities = list(str(city) for city in Location.objects.filter(country_short=country_id))
    return JsonResponse({"cities": cities})