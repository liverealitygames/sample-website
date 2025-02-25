from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.http import JsonResponse

from community.const import GAME_FORMATS, DEFAULT_BANNERS
from posts.models import Post
from community.models import Season
from homepage.models import Location
from posts.const import COUNTRIES, STATES

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
    casting_posts = Post.objects.filter(season__status="Casting")
    casting_country_ids = {post.season.location.country_short for post in casting_posts}
    casting_state_ids = {post.season.location.region_short for post in casting_posts}
    context = {
        "countries": ((country_short,country_long) for country_short,country_long in COUNTRIES.items() if country_short in casting_country_ids),
        "states": ((state_short,state_long) for state_short,state_long in STATES.items() if state_short in casting_state_ids),
        "formats": GAME_FORMATS,
        "binary_filters": [("Filmed only", "filmed")],
        "default_banners": DEFAULT_BANNERS.items(),
    }

    if request.method == "POST":
        country_short = request.POST.get("countrySelected", None)
        city = request.POST.get("citySelected", None)
        state_short = request.POST.get("stateSelected", None)
        game_format = request.POST.get("gameFormat", None)
        query = request.POST.get("query", None)

        # Optimize location filtering
        locations = Location.objects.all()
        if country_short:
            locations = locations.filter(country_short=country_short)
        if state_short:
            locations = locations.filter(region_short=state_short)
        if city:
            city = city.split(",")[0]
            locations = locations.filter(city=city)

        # Optimize post filtering
        posts = casting_posts.select_related("season").prefetch_related("season__location")

        if game_format:
            posts = posts.filter(season__format=game_format)

        if query:
            posts = posts.annotate(
                search=SearchVector("description", "season__name", "season__format")
            ).filter(search=SearchQuery(query))

        if country_short or state_short or city:
            locations_list = locations.values_list("id", flat=True)
            posts = posts.filter(season__location_id__in=locations_list)

        context.update({"posts": posts})

    return render(request, "posts/search.html", context)


# AJAX

def get_cities(request):
    country_id = request.GET.get("country_id")
    cities = list(str(city) for city in Location.objects.filter(country_short=country_id))
    return JsonResponse({"cities": cities})