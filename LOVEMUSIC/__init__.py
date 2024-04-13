from LOVEMUSIC.core.bot import LOVE
from LOVEMUSIC.core.dir import dirr
from LOVEMUSIC.core.git import git
from LOVEMUSIC.core.userbot import Userbot
from LOVEMUSIC.misc import dbb, heroku
from telethon import TelegramClient
from config import API_ID, API_HASH

from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = LOVE()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()

telethn = TelegramClient("LOVEMUSIC", API_ID, API_HASH)
