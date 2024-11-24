import json
import os

from LOVEMUSIC.core.bot import LOVEBot
from LOVEMUSIC.core.dir import dirr
from LOVEMUSIC.core.git import git
from LOVEMUSIC.core.userbot import Userbot
from LOVEMUSIC.core.youtube import GOKUBLACK
from LOVEMUSIC.misc import dbb, heroku, sudo

from .logging import LOGGER

dirr()

git()

dbb()

heroku()

sudo()

GOKUBLACK()

app = LOVEBot()

userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
HELPABLE = {}
