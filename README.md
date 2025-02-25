# Sample Website

## General

### Online Access

The latest version of the website should be available at [https://lrg-demo.jayvivor.com](https://lrg-demo.jayvivor.com) . This version is populated with fake data that is shared between everyone who accesses it.
If the online version has issues, you could also run a local copy of this website with these steps:

#### Spinning Up
 
1. Install and run Docker Desktop: https://docs.docker.com/compose/install/
2. Download this repository and extract it to a folder: https://github.com/liverealitygames/sample-website/archive/refs/heads/main.zip 
3. Open a [terminal/command prompt](https://www.wikihow.com/Open-Terminal-in-Windows) in the same folder as the repository, and run `docker compose up`. When you see something like `lrg             | Watching for file changes with StatReloader`, that means the server is up and running. You can move on to the next step. (This may take longer on older systems with less space)
    - If this gives you an error, make sure you're in the same folder as the file `docker-compose.yaml`. If not, open a new terminal in that folder and try again.
5. Open a web browser and go to `localhost:8080`. You should see the home screen.

#### Making Changes

You can login to the admin console by going to `localhost:8080/admin`, with "admin" as the username and "password" as the password. These credentials only work locally. From here, you will be able to manually create, destroy, or change any of the resources that appear on the main page - the communities, the posts, the seasons, the podcasts, the news articles, etc.

Running the website locally means any changes to website-related files should update automatically - for example, if you go to `../src/lrg/homepage/templates/homepage/base.html`, change line 7 from `<title>LRG Demo</title>` to `<title>My Site</title>`, and save the file, that change should be reflected when you go back to view the page. There are exceptions to this; some changes to the `models.py` files will require you to perform a "migration" of the data, as the database needs to update its schema based on how the models have changed.

#### Spinning Down

When you're finished, you can stop the service in a few ways:

- If the terminal running the service is still open, re-enter it and press `CTRL-C` (On Windows), OR
- If not, re-enter the folder with the `docker-compose.yaml` file and run `docker compose stop && docker compose rm` (press "y" when prompted), OR
- Stop the container in the UI.

None of the above should delete any modifications you have made.

#### Deleting

When docker "spins up" the website, it creates files on your disk that can become quite large and may persist even after docker is uninstalled. If you want to remove everything associated with this website from your computer, you will need to remove those files before uninstalling docker. There are `docker compose` commands that let you do this, but the easiest way is to open up docker desktop, stop any running containers (if applicable), and then go to your images and delete those as well.

After removing all containers and images you should be okay to uninstall docker.

### Contact and Support

- If you need help, email me at jayvivor@gmail.com

--

## Technical Details

### Project Overview

- Right now, the features that are (at least partially) implemented include:
    - Basic user/profile/admin system
    - Ability for users to create communities, seasons, and posts
    - Include links to other resources and contact information for a community (social media handles, wiki, etc)
    - Links to podcasts, news, etc.

### Tech Stack

- I used Bootstrap/Django/Postgres/GCP as those are the tools I am most comfortable with. I am not married to them and they do cost more money and require more maintenance than other options (GCP especially).

### Installation Notes

Some extra configuration options:

- By default, every time you spin up/spin down the website, it will run a script to completely reset the database. This can be annoying if you'd prefer communities/posts/etc you have created to persist. You can change this behavior by setting the `FULL_RESET_DB` environment variable to `False` on deployment.
- The fake data populated by the startup/database reset script can be found in `src/lrg/homepage/management/commands/*.py`. I've limited the number of locations and profiles that are created for performance reasons, but feel free to tweak those values or skip the step altogether.

### Deployment Notes

The infrastructure is managed by another repo in this organization - email me if you are curious or want access to it.
