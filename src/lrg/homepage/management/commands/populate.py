from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker
from faker.providers.person.en import Provider
from profiles.models import Profile
from community.models import Community, Season, Schedule, ContactInfo, Staff
from homepage.models import Location
from community.const import SEASON_STATUSES, GAME_FORMATS, COMMUNITY_STATUSES
from posts.models import Post
from media.models import Podcast, Article
import random
import os

fake = Faker()

suffixes = ["-Vivor", "'s Big Brother", "'s The Challenge", "'s Survivor", "'s Reality Games", " Does RGs", " Reality Gaming", " LRGs", " RG Hub"]

def fake_org_names(num):
    if num > len(Provider.first_names):
        raise ValueError("Not enough first names for the number of users requested")
    fake_names = random.choices(Provider.first_names, num)
    names = [name+random.choice(suffixes) for name in fake_names]
    return names

def fake_org_name(faker):
    return faker.unique.first_name()+random.choice(suffixes)

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=100, help='Number of users to create')
        parser.add_argument('--communities', type=int, default=50, help='Number of communities to create')
        parser.add_argument('--seasons', type=int, default=10, help='Max number of seasons per community')

    def handle(self, *args, **kwargs):

        help = 'Populate the database with fake data'

        lorem_ipsum = "Lorem ipsum odor amet, consectetuer adipiscing elit. Sem cubilia fermentum lectus consequat risus, amet mattis cras. Aliquet quis nisl nec accumsan et himenaeos imperdiet aliquet."

        non_latest = SEASON_STATUSES.copy()
        non_latest.remove("Casting")
        latest = SEASON_STATUSES.copy()

        users = int(kwargs["users"])
        communities = int(kwargs["communities"])
        seasons = int(kwargs["seasons"])

        # Users and Profiles
        print("users")
        self.stdout.write(f"Creating {users} dummy users... ", ending='')
        fake_users = User.objects.bulk_create(
            [User(username=fake.unique.user_name(), password="password") for _ in range(kwargs["users"])]
        )
        self.stdout.write(self.style.SUCCESS('OK'))
        
        self.stdout.write(f"Creating {users} dummy profiles... ", ending='')
        fake_profiles = Profile.objects.bulk_create(
            [
                Profile(
                    user=user,
                    account_status="Active",
                    auth_source="Internal",
                    pronouns=random.choice(["he/him","she/her","they/them","any pronouns"]),
                    creation_time=fake.date_time_this_month(),
                    ) for user in fake_users
            ]
        )
        
        superuser = User.objects.get(username=os.environ.get("DJANGO_SUPERUSER_USERNAME"))
        Profile.objects.create(
            user=superuser,
            account_status="Active",
            auth_source="Internal",
        )
        self.stdout.write(self.style.SUCCESS('OK'))
        
        # Communities and Seasons
        self.stdout.write(f'Creating {communities} dummy communities... ', ending='')
        communities = Community.objects.bulk_create(
            [
                Community(
                    name=fake_org_name(fake),
                    description=lorem_ipsum,
                    owner=random.choice(fake_profiles),
                    status=random.choice(COMMUNITY_STATUSES),
                ) for _ in range(kwargs["communities"])
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write(f'Creating dummy contact info for communities... ', ending='')
        contacts = []
        for community in communities:
            # 50/50 that they have contact info for each criteria
            wiki = "https://bigbrother.fandom.com/wiki/David_Alexander" if random.choice([True, False]) else None
            instagram = "@somehandle" if random.choice([True, False]) else None
            facebook = "https://www.facebook.com/Survivor/" if random.choice([True, False]) else None
            youtube = "https://www.youtube.com/watch?v=jNQXAC9IVRw" if random.choice([True, False]) else None
            other_link = "https://x.com/amazingracecbs" if random.choice([True, False]) else None

            contacts.append(ContactInfo(
                community=community,
                wiki=wiki,
                instagram=instagram,
                facebook=facebook,
                youtube=youtube,
                other_link=other_link,
            ))
            
        contacts = ContactInfo.objects.bulk_create(contacts)
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Setting staff for dummy communities... ', ending='')
        for community in communities:
            potential_staff = random.sample(fake_profiles, random.randint(1,5))
            staff = Staff(community=community)
            staff.save()
            staff.hosts.set([community.owner])
            staff.contacts.set([community.owner])
            staff.general.set(potential_staff)
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write(f"Creating 1-{seasons} dummy seasons for each community... ", ending='')
        per_season = []
        us_locations = Location.objects.all().filter(country="United States")
        all_locations = Location.objects.all()
        for community in communities:
            format = random.choice(GAME_FORMATS)
            international = random.choice([True, False])
            total_seasons = random.randint(1,kwargs["seasons"])
            for number in range(1,total_seasons):
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
                        creation_time=fake.unique.date_time_this_month(),
                        status=random.choice(non_latest) if number < (total_seasons - 1) else random.choice(latest),
                        number=number,
                        community=community,
                        format=format,
                        location=random.choice(all_locations if international else us_locations),
                        schedule=schedule,
                        application_link="https://forms.gle/umLWkHNwkKxH6sEu8",
                        )
                    )
        seasons = Season.objects.bulk_create(per_season)
        self.stdout.write(self.style.SUCCESS(f"OK ({len(seasons)})"))

        self.stdout.write('Setting dummy cast for each season... ', ending='')
        for season in seasons:
            season.cast.set(random.sample(fake_profiles, min(random.randint(10,20), len(fake_profiles))))
        self.stdout.write(self.style.SUCCESS(f"OK"))

        # Posts
        self.stdout.write('Creating dummy posts for each season... ', ending='')
        posts = [
                Post(
                    description=lorem_ipsum,
                    creation_time=season.creation_time,
                    season=season,
                ) for season in seasons
            ]
        Post.objects.bulk_create(posts, batch_size=500)
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