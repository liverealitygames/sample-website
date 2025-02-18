from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from community.const import GAME_FORMATS
from posts.models import Post

def browse(request):
    posts = Post.objects.filter(season__status="Casting")
    return render(request, "posts/browse.html", context={"posts":posts})

@login_required
def create(request):
    return render(request, "posts/create.html", context={"game_formats":GAME_FORMATS})

def info(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "posts/info.html", context={"post":post})

def search(request):
    posts = Post.objects.filter(season__status="Casting")
    return render(request, "posts/info.html", context={"posts":posts})