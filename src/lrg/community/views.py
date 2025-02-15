from django.shortcuts import render

from dataclasses import dataclass

import random
from community.const import COMMUNITY_STATUSES

@dataclass
class DummyCommunity:
    name: str
    status: str
    owner: str

    def __str__(self):
        return self.name

communities = [
    "CozyHaven",
    "StarlightForum",
    "PixelGarden",
    "Dreamer’s Nook",
    "The Chat Loft",
    "Harmony Hub",
    "Serene Circles",
    "Wanderer's Cove",
    "GoldenThreads",
    "Sapphire Haven",
    "LushMeadows",
    "The Whimsy Club",
    "CottageCloud",
    "Velvet Echo",
    "Sunbeam Collective",
    "Nebula Nest",
    "ChatterBloom",
    "Twilight Harbor",
    "BreezyForum",
    "Aurora Lounge"
]

fake_names = [
    "ShadowProwler99",
    "NeonPhantomX",
    "CyberNinja42",
    "PixelWarrior77",
    "GlitchVortex",
    "QuantumFalcon",
    "EchoSpecter",
    "ZeroGravityX",
    "ByteCrusher",
    "StealthHavoc",
    "OblivionStriker",
    "DarkMatterWolf",
    "InfinityCircuit",
    "RetroByteKnight",
    "WarpSpeedX",
    "FrostByte99",
    "SpectralRogue",
    "VortexViper",
    "CrimsonSpecter",
    "LunarEcho99",
    "LunaBloom",
    "CherryWhimsy",
    "RosieGlow",
    "StarrySkye",
    "PetalDancer",
    "SugarPlume",
    "SunnyLark",
    "VelvetDaisy",
    "PearlMelody",
    "MistyFawn",
    "LavenderHaze",
    "DewdropBreeze",
    "GoldenMarigold",
    "SereneWillow",
    "BlossomCharm",
    "BreezyLyric",
    "HoneyLace",
    "StarlitMeadow",
    "DaisyWhisper",
    "MoonlitLily",
]

dummy_communities = [DummyCommunity(name=community_name, 
                 status=random.choice(COMMUNITY_STATUSES),
                 owner=random.choice(fake_names)) for community_name in communities]

# Create your views here.
def browse(request):
    return render(request, "community/browse.html", context={"sample_data":dummy_communities})

def create(request):
    return render(request, "community/create.html")

def info(request, community_id):
    return render(request, "community/info.html")