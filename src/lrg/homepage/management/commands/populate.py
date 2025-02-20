from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker
from profiles.models import Profile
from community.models import Community, Season, Schedule
from homepage.models import Location
from community.const import SEASON_STATUSES, GAME_FORMATS, COMMUNITY_STATUSES
from posts.models import Post
from media.models import Podcast, Article
import random
import os

fake = Faker()

def fake_org_names(num):
    names = []
    while len(names) < num:
        prefix = fake.first_name()
        suffix = random.choice(["-Vivor", "'s Big Brother", "'s The Challenge", "'s Survivor", "'s Reality Games", " Does RGs", " Reality Gaming", " LRGs", " RG Hub"])
        if prefix+suffix not in names:
            names.append(prefix+suffix)
    return names

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):

        help = 'Populate the database with fake data'

        # Users and Profiles
        print("users")
        self.stdout.write('Creating dummy users... ', ending='')
        fake_users = User.objects.bulk_create(
            [User(username=fake.profile()["username"], password=make_password(fake.password())) for _ in range(100)]
        )
        self.stdout.write(self.style.SUCCESS('OK'))
        
        self.stdout.write('Creating dummy profiles... ', ending='')
        fake_profiles = [Profile.objects.create(
                user=user,
                account_status="Active",
                auth_source="Internal",
                pronouns=random.choice(["he/him","she/her","they/them","any pronouns"]),
                creation_time=fake.date_time_this_month(),
            ) for user in fake_users]
        
        superuser = User.objects.get(username=os.environ.get("DJANGO_SUPERUSER_USERNAME"))
        Profile.objects.create(
            user=superuser,
            account_status="Active",
            auth_source="Internal",
        )
        self.stdout.write(self.style.SUCCESS('OK'))
        
        # Communities and Seasons
        self.stdout.write('Creating dummy communities... ', ending='')
        community_size = 50
        fake_org_name_list = fake_org_names(community_size)
        communities = Community.objects.bulk_create(
            [
                Community(
                    name=fake_org_name,
                    description=fake.paragraph(nb_sentences=3),
                    owner=random.choice(fake_profiles),
                    status=random.choice(COMMUNITY_STATUSES),
                ) for fake_org_name in fake_org_name_list
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Setting staff for dummy communities... ', ending='')
        for community in communities:
            community.staff.set(random.sample(fake_profiles, random.randint(1,5)))
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Creating dummy seasons for each community... ', ending='')
        per_season = []
        us_locations = Location.objects.all().filter(country="United States")
        all_locations = Location.objects.all()
        for community in communities:
            format = random.choice(GAME_FORMATS)
            international = random.choice([True, False])
            for number in range(1,random.randint(1,8)):
                start_date = fake.date_this_year()
                duration = random.randint(1,10)
                isFuzzy = random.choice([True, False])
                if isFuzzy:
                    schedule = Schedule(
                        start_time_specific=start_date,
                        game_length_range_exact=duration,
                    )
                else:
                    schedule = Schedule(
                        start_time_range_earliest=start_date,
                        game_length_range_exact=duration,
                    )
                schedule.save()
                per_season.append(
                    Season(
                        creation_time=fake.date_time_this_month(),
                        status=random.choice(SEASON_STATUSES),
                        number=number,
                        community=community,
                        format=format,
                        location=random.choice(all_locations if international else us_locations),
                        schedule=schedule
                        )
                    )
        seasons = Season.objects.bulk_create(per_season)
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Setting dummy staff for each season... ', ending='')
        for season in seasons:
            season.staff.set(community.staff.all())
            non_staff = [profile for profile in fake_profiles if profile not in season.staff.all()]
            season.cast.set(random.sample(non_staff, min(random.randint(10,20), len(non_staff))))
        self.stdout.write(self.style.SUCCESS('OK'))

        # Posts
        self.stdout.write('Creating dummy posts for each season... ', ending='')
        posts = Post.objects.bulk_create(
            [
                Post(
                    description=fake.paragraph(),
                    creation_time=season.creation_time,
                    season=season,
                ) for season in seasons
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Creating dummy media... ', ending='')
        Podcast.objects.create(
            title="Rob Has a Podcast",
            embed="https://robhasawebsite.com/",
            source="Spotify",
            description="Rob Has a Podcast is about a guy named Taran who has a podcast."
        )
        Podcast.objects.create(
            title="No Buffs",
            embed="https://open.spotify.com/show/0EVPiYK0o4tfP5NbkO9BuM",
            source="Spotify",
            description="People talk about Survivor on this one."
        )
        Podcast.objects.create(
            title="The Pod Has Spoken",
            embed="https://www.theringer.com/podcasts/the-pod-has-spoken",
            source="Spotify",
            description="Tyson, who has played survivor, talks about survivor."
        )
        Podcast.objects.create(
            title="A Tribe Called Best",
            embed="https://open.spotify.com/show/0EVPiYK0o4tfP5NbkO9BuM",
            source="Spotify",
            description="Musicians discuss the latest episode of survivor, despite having never seen it."
        )

        Article.objects.create(
            title="Shocking! Big Brother Blinks for First Time in Years",
            embed="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            description="As it turns out, Big Brother is only sometimes watching. Other times he decides to blink. We followed Big Brother for..."
        )
        Article.objects.create(
            title="Area Man Runs into Johnny Bananas in-Person, Does not Recognize Him",
            embed="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            description="Who does this guy think he is? As Milwaukee resident Harris Brown exited a coffee shop, he unwittingly ran into a..."
        )
        self.stdout.write(self.style.SUCCESS('OK'))


        self.stdout.write(self.style.SUCCESS('Dummy data populated.'))
