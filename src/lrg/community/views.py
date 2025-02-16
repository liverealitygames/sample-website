from django.shortcuts import render, get_object_or_404
from community.models import Community, Season

# Create your views here.
def browse(request):
    communities = Community.objects.all()
    return render(request, "community/browse.html", context={"communities":communities})

def create(request):
    return render(request, "community/create.html")

def community_info(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    return render(request, "community/community_info.html", context={"community":community})

def season_info(request, community_id, season_id):
    # TODO: Staff and owners see a different UI
    season = get_object_or_404(Season, id=season_id)
    return render(request, "community/season_info.html", context={"season":season})