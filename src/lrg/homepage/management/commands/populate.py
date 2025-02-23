import sqlite3
import random
import os
from faker import Faker
from faker.providers.person.en import Provider
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from community.const import SEASON_STATUSES, GAME_FORMATS, COMMUNITY_STATUSES

fake = Faker()


def fake_org_names(num):
    if num > len(Provider.first_names):
        raise ValueError("Not enough first names for the number of users requested")
    fake_names = random.choices(Provider.first_names, num)
    suffixes = ["-Vivor", "'s Big Brother", "'s The Challenge", "'s Survivor", "'s Reality Games", " Does RGs", " Reality Gaming", " LRGs", " RG Hub"]
    names = [name + random.choice(suffixes) for name in fake_names]
    return names


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=100, help='Number of users to create')
        parser.add_argument('--communities', type=int, default=50, help='Number of communities to create')
        parser.add_argument('--seasons', type=int, default=10, help='Max number of seasons per community')

    def handle(self, *args, **kwargs):
        db_path = "db.sqlite3"  # Adjust path if necessary
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # **1. Users and Profiles**
        self.stdout.write('Creating dummy users...', ending='')
        users_data = [(fake.profile()["username"], make_password(fake.password())) for _ in range(kwargs["users"])]
        cursor.executemany("INSERT INTO auth_user (username, password, is_active) VALUES (?, ?, 1)", users_data)
        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))

        self.stdout.write('Creating dummy profiles...', ending='')
        cursor.execute("SELECT id FROM auth_user")
        user_ids = [row[0] for row in cursor.fetchall()]
        profiles_data = [(uid, "Active", "Internal", random.choice(["he/him", "she/her", "they/them", "any pronouns"])) for uid in user_ids]
        cursor.executemany("INSERT INTO profiles_profile (user_id, account_status, auth_source, pronouns) VALUES (?, ?, ?, ?)", profiles_data)
        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))

        # **2. Communities**
        self.stdout.write('Creating dummy communities...', ending='')
        fake_org_name_list = fake_org_names(kwargs["communities"])
        community_data = [(name, fake.paragraph(nb_sentences=3), random.choice(user_ids), random.choice(COMMUNITY_STATUSES)) for name in fake_org_name_list]
        cursor.executemany("INSERT INTO community_community (name, description, owner_id, status) VALUES (?, ?, ?, ?)", community_data)
        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))

        # **3. Seasons**
        self.stdout.write('Creating dummy seasons...', ending='')
        cursor.execute("SELECT id FROM community_community")
        community_ids = [row[0] for row in cursor.fetchall()]
        
        season_data = []
        for community_id in community_ids:
            format = random.choice(GAME_FORMATS)
            for number in range(1, random.randint(1, kwargs["seasons"])):
                status = random.choice(SEASON_STATUSES)
                season_data.append((status, number, community_id, format))

        cursor.executemany("INSERT INTO community_season (status, number, community_id, format) VALUES (?, ?, ?, ?)", season_data)
        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))

        # **4. Posts**
        self.stdout.write('Creating dummy posts...', ending='')
        cursor.execute("SELECT id FROM community_season")
        season_ids = [row[0] for row in cursor.fetchall()]
        post_data = [(fake.paragraph(), random.choice(season_ids)) for _ in range(len(season_ids))]
        cursor.executemany("INSERT INTO posts_post (description, season_id) VALUES (?, ?)", post_data)
        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))

        # **5. Media (Podcasts & Articles)**
        self.stdout.write('Creating dummy media...', ending='')
        podcasts = [
            ("Rob Has a Podcast", "https://robhasawebsite.com/", "Spotify", "Rob Has a Podcast is about a guy named Taran who has a podcast."),
            ("No Buffs", "https://open.spotify.com/show/0EVPiYK0o4tfP5NbkO9BuM", "Spotify", "People talk about Survivor on this one."),
            ("The Pod Has Spoken", "https://www.theringer.com/podcasts/the-pod-has-spoken", "Spotify", "Tyson, who has played survivor, talks about survivor."),
            ("A Tribe Called Best", "https://open.spotify.com/show/0EVPiYK0o4tfP5NbkO9BuM", "Spotify", "Musicians discuss the latest episode of survivor, despite having never seen it."),
        ]
        cursor.executemany("INSERT INTO media_podcast (title, embed, source, description) VALUES (?, ?, ?, ?)", podcasts)

        articles = [
            ("Shocking! Big Brother Blinks for First Time in Years", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "As it turns out, Big Brother is only sometimes watching. Other times he decides to blink."),
            ("Area Man Runs into Johnny Bananas in-Person, Does not Recognize Him", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "Who does this guy think he is? A Milwaukee resident ran into a reality star and didn't even know it."),
        ]
        cursor.executemany("INSERT INTO media_article (title, embed, description) VALUES (?, ?, ?)", articles)

        conn.commit()
        self.stdout.write(self.style.SUCCESS('OK'))
        conn.close()

        self.stdout.write(self.style.SUCCESS('Dummy data populated.'))
