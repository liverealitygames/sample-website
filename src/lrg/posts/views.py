from django.shortcuts import render

from dataclasses import dataclass

import random
from posts.const import GAME_FORMATS

@dataclass
class DummyORG:
    name: str
    season_number: int
    start_date: str
    logo_url: str

    def __str__(self):
        return self.name

lrg_names = ["ORGVivor","Amazing Grace","Little Sister"]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
years = ["2026", "2027", "2028"]
image_urls = [
        "https://static1.srcdn.com/wordpress/wp-content/uploads/2020/01/Survivor-Logo-2.jpg",
        "https://www.bellmedia.ca/lede/wp-content/uploads/2023/06/TARC_Logo_Colour.jpg",
        "https://upload.wikimedia.org/wikipedia/en/b/be/Big_Brother_%28Franchise%29_2019_Logo.jpg",
]

orgs = [DummyORG(name=orgname, 
                 season_number=random.randint(1,20), 
                 logo_url=random.choice(image_urls),
                 start_date=f"{random.choice(months)} {random.choice(years)}") for orgname in lrg_names]

# Create your views here.

def browse(request):
    return render(request, "posts/browse.html", context={"sample_data":orgs})

def create(request):
    return render(request, "posts/create.html", context={"game_formats":GAME_FORMATS})

def info(request, post_id):
    return render(request, "posts/create.html", context={"game_formats":GAME_FORMATS})