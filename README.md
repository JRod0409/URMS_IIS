# URMS_IIS
URMS is a user-rated-music-site where users rate and add songs to find objectively good music. It utilizes Spotify API and basic database filtering to provide song results for users to rate and explore. URMS_IIS is the branch deployed on Windows IIS for https://urms.live. The app was developed by Spence Peters, John Williams, and Jacob Rodriguez.

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

[![Deploy Django on Windows using Microsoft IIS by Johnnyboycurtis on YouTube.](https://img.youtube.com/vi/APCQ15YqqQ0/0.jpg)](https://www.youtube.com/watch?v=APCQ15YqqQ0)
## Deployment

Once you have bound the website to a domain or public IP address and you have port forwarded the IP address of your site, you can run and test the website.
```python
  cd C:\inetpub\urms\URMS-FinalProject\FinalProject

  python manage.py runserver
```
The tutorial is bare bones, but it should be a good place to start if you would like to replicate this project.
