from django.shortcuts import render

# Create your views here.

def news(request):
    return render(request, 'media/news.html')

def podcasts(request):
    return render(request, 'media/podcasts.html')