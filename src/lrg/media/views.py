from django.shortcuts import render
from media.models import Podcast, Article

# Create your views here.

def news(request):
    return render(request, 'media/news.html', context={"articles":Article.objects.all()})

def podcasts(request):
    return render(request, 'media/podcasts.html', context={"podcasts":Podcast.objects.all()})