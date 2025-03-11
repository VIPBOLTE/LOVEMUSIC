import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", None))

# Get this value from @TheChampuBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 6399386263))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/VIPBOLTE/LOVEMUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/channelz_k")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/goku_groupz")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", None
)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
TEMP_DB_FOLDER = "tempdb"

START_IMG_URL = getenv(
    "START_IMG_URL", "https://envs.sh/s/IB5qmR6tODPCcNm6NAmuHA/Wds.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://envs.sh/s/LgsoI5FAzsCpZ5UecZCzDQ/W2K.jpg"
)
PLAYLIST_IMG_URL = "https://envs.sh/s/IB5qmR6tODPCcNm6NAmuHA/Wds.jpg"
STATS_IMG_URL = "https://envs.sh/s/zPGmxpcYcoARRIQqQtyVfw/WdM.jpg"
TELEGRAM_AUDIO_URL = "https://envs.sh/s/NEuDeMOOP0JU5BSmAY7gSA/Wdm.jpg"
TELEGRAM_VIDEO_URL = "https://envs.sh/s/i0YWsoZ6cUhL7EZO79EQqQ/WdO.jpg"
STREAM_IMG_URL = "https://envs.sh/s/4ht29RFA5a1P_9XMK19pPA/Wdx.jpg"
SOUNCLOUD_IMG_URL = "https://envs.sh/s/WV85h_s_uMx8BrD5HmA1wA/Wd-.jpg"
YOUTUBE_IMG_URL = "https://envs.sh/s/1l39K1DNRg6DRCag0k_4iQ/W20.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://envs.sh/s/a1aYFyCzf4FKZu7e1pJovQ/W2q.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://envs.sh/s/tRhUQrmd-HpxKjmyxhEGNA/W2w.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://envs.sh/s/YkamjVd3r_qatS0nQeCcJg/W2u.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# Set it true if you want your bot to be private only [You'll need to allow CHAT_ID via /authorize command then only your bot will play music in that chat.]
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", "False")

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
)
