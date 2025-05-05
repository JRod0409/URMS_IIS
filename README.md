# URMS_IIS
URMS is a user-rated-music-site where users rate and add songs to find objectively good music. It utilizes Spotify API and basic database filtering to provide song results for users to rate and explore. URMS_IIS is the branch deployed on Windows IIS for https://urms.live. The app was developed by Spence Peters, John Williams, and Jacob Rodriguez.

## Jump to different sections

- [Installation](#installation)
- [Deployment](#Deployment)
- [User Examples](#User-Examples)
- [Home page usage](#Home-page-usage)
- [Browse page usage](#Browse-page-usage)
- [Profile page usage](#Profile-page-usage)

## Dependencies

- django
- pillow
- spotipy
- wfastcgi
- openpyxl
## Installation

Navigate to **C:\inetpub** and create a new directory on a server with IIS installed.

```cmd
  cd C:\inetpub
  git clone https://github.com/JRod0409/urms_IIS.git
```

Install the following python libraries:
```python
  pip install django
  pip install pillow
  pip install spotipy
  pip install wfastcgi
  pip install openpyxl
```

**Follow this tutorial by Johnnyboycurtis on YouTube for proper IIS configuration.**

[![Deploy Django on Windows using Microsoft IIS by Johnnyboycurtis on YouTube.](https://img.youtube.com/vi/APCQ15YqqQ0/0.jpg)](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE)
## Deployment

Once you have bound the website to a domain or public IP address and you have port forwarded the IP address of your site, you can run and test the website.
```python
  cd C:\inetpub\urms\URMS-FinalProject\FinalProject

  python manage.py runserver
```
The tutorial is bare bones, but it should be a good place to start if you would like to replicate this project.
## User Examples
The following are some brief examples of how the user is able to interact with the site. This includes where users can find music, how they rate it, and how they can add their favorite songs to the website themselves.

### Home page usage:

![Homepage](https://keyboardmechanic.com/img/website-screenshot-1.png)

**The nav bar has three options: home, browse, profile and login/logout.**

When you click home, the home page features a hero section that displays the top song of the week. This is determined user ratings during the week of viewing, and users have the option to rate it to see if the rating is fair. After this is the top artists of the week section. 

This display only section draws the three most popular artists by finding the average score of their music.

![Random song lineup](https://keyboardmechanic.com/img/random-song-lineup.png)

The random song lineup section picks five random songs from the database 100% indiscriminately. Using the combination of homepage sections, users will always be able to interact with the key features of the site.

### Browse page usage:

![Browse](https://keyboardmechanic.com/img/website-screenshot-2.png)

**The browse section is designed to find specific songs the user is looking for.**

Use the sort by dropdown to sort results by Title, Artist, Genre, Score, Releasedate. The user can then rate using the rate button next to each song.

![Browse2](https://keyboardmechanic.com/img/music-section.png)

Access the detail menu for any song in the browser by clicking the item.

### Profile page usage:

![Profile](https://keyboardmechanic.com/img/profile-1.png)

**The key usage of this section other than editing your email is to add a song.**

![Profile2](https://keyboardmechanic.com/img/profile-2.png)

You add a song by pasting the song link and clicking add song. You can find the song link of any track on Spotify by finding your song → clicking the three dots → share → copy song link.

**This concludes the core user features of the site.**
