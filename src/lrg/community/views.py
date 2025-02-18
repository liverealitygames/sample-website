from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from community.models import Community, Season, Schedule
from homepage.models import Country, Location
from community.const import GAME_FORMATS


# Create your views here.
def browse(request):
    communities = Community.objects.all()
    return render(request, "community/browse.html", context={"communities":communities})

@login_required
def create_community(request):
    if request.method == "POST":
        data = {
            "name": request.POST("communityName"),
            "description": request.POST("discussion"),
            "owner": request.user,
            "status": "Under Review",
            }

        community = Community(**data)  # Initialize the object

        try:
            community.full_clean()  # Run validation
            community.save()  # Save if valid
            messages.success(request, "Account created successfully")
            return redirect("login")
        except ValidationError as e:
            messages.error(request, f"Error creating community. {e}")

    return render(request, "community/create.html")

@login_required
def create_season(request):
    if request.method == "POST":

        community = get_object_or_404(Community, request.POST("communitySelected"))
        location = get_object_or_404(Location, country=request.POST("countrySelected"), city=request.POST("citySelected"))

        schedule_data = {
            "game_length_range_exact": request.POST("gameLength"),
            ("start_time_specific" if request.POST("fuzzyStartDate") else "start_time_earliest"): request.POST("startDate"),
        }

        schedule = Schedule(**schedule_data)

        season_data = {
            "name": request.POST("seasonName"),
            "number": request.POST("seasonNumber"),
            "description": request.POST("discussion"),
            "status": "Under Review",
            "filmed": request.POST("filmed", False),
            "community":community,
            "status": "Under Review",
            "location":location,
            "application_link": request.POST("applicationLink", ""),
            "format": request.POST("formatSelected"),
        }

        season = Season(**season_data)  # Initialize the object

        try:
            schedule.full_clean()
            schedule.save()
            season.full_clean()
            season.save()
            messages.success(request, "Season created successfully")
            return redirect("community:season_info", community_id=community.id, season_id=season.id)
        except ValidationError as e:
            messages.error(request, f"Error creating community. {e}")

    return render(request, "community/create.html", context={
        "countries": list(Country.objects.values("id", "name")),
        "formats": GAME_FORMATS,
        }
    )

def community_info(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    return render(request, "community/community_info.html", context={"community":community})

def season_info(request, community_id, season_id):
    # TODO: Staff and owners see a different UI
    season = get_object_or_404(Season, id=season_id)
    return render(request, "community/season_info.html", context={"season":season})