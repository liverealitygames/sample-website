from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from profiles.models import Profile
from community.models import Community, Season
from community.const import SEASON_STATUSES, GAME_FORMATS, COMMUNITY_STATUSES
from posts.models import Post
import random
import os

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):

        help = 'Populate the database with fake data'

        self.stdout.write('Creating dummy users... ', ending='')
        fake_users = [User.objects.create_user(username = fake.profile()["username"]) for _ in range(20)]
        self.stdout.write(self.style.SUCCESS('OK'))
        
        self.stdout.write('Creating dummy profiles... ', ending='')
        fake_profiles = [Profile.objects.create(
                user=user,
                account_status="Active",
                auth_source="Internal",
                creation_time=fake.date_time_this_month(),
            ) for user in fake_users]
        
        superuser = User.objects.get(username=os.environ.get("DJANGO_SUPERUSER_USERNAME"))
        Profile.objects.create(
            user=superuser,
            account_status="Active",
            auth_source="Internal",
        )
        self.stdout.write(self.style.SUCCESS('OK'))
        
        self.stdout.write('Creating dummy communities... ', ending='')
        communities = Community.objects.bulk_create(
            [
                Community(
                    name=fake.company(),
                    description=fake.paragraph(nb_sentences=3),
                    owner=random.choice(fake_profiles),
                    status=random.choice(COMMUNITY_STATUSES),
                ) for _ in range(5)
            ]
        )
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Setting staff for dummy communities... ', ending='')
        for community in communities:
            community.staff.set(random.sample(fake_profiles, random.randint(1,5)))
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Creating dummy seasons for each community... ', ending='')
        per_season = []
        for community in communities:
            format = random.choice(GAME_FORMATS)
            for number in range(random.randint(1,8)):
                per_season.append(
                    Season(
                        creation_time=fake.date_time_this_month(),
                        status=random.choice(SEASON_STATUSES),
                        number=number,
                        community=community,
                        format=format,
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

        self.stdout.write(self.style.SUCCESS('Dummy data populated.'))
