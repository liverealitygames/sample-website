from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator

from community.const import GAME_FORMATS
from posts.models import Post
from homepage.models import Country
from community.models import Season

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
        query = request.POST.get("query", None)
        if query:
            print(query)
            posts = Post.objects.annotate(
                search=SearchVector("description","season__name","season__format"),
            ).filter(search=query)
        else:
            print("No query")
            posts = Post.objects.all()

        return render(request, 'posts/search.html', context={
            "countries": list(Country.objects.values("id", "name")),
            "binary_filters": [
                ("Filmed only", "filmed"),
            ],
            "posts":posts,
        })

    return render(request, 'posts/search.html', context={
        "countries": list(Country.objects.values("id", "name")),
        "binary_filters": [
            ("Filmed only", "filmed"),
        ]
    })