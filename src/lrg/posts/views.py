from django.shortcuts import render

from community.const import GAME_FORMATS
from posts.models import Post


def browse(request):
    posts = Post.objects.filter(season__status="Casting")
    return render(request, "posts/browse.html", context={"sample_data":posts})

def create(request):
    return render(request, "posts/create.html", context={"game_formats":GAME_FORMATS})

def info(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "posts/info.html", context={"post":post})