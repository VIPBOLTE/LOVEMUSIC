import asyncio
import os
import re
import json
import glob
import random
import logging
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from LOVEMUSIC.utils.database import is_on_off
from LOVEMUSIC.utils.formatters import time_to_seconds

# ───────────────────── LOGGER ───────────────────── #

log = logging.getLogger("YouTube")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ───────────────────── COOKIE HANDLER ───────────────────── #

COOKIE_DIR = os.path.join(os.getcwd(), "cookies")

def get_cookie_file() -> str:
    cookies = glob.glob(os.path.join(COOKIE_DIR, "*.txt"))
    if not cookies:
        raise FileNotFoundError("No cookie files found in /cookies")

    cookie = random.choice(cookies)
    log.info(f"Using cookie: {os.path.basename(cookie)}")
    return cookie

# ───────────────────── YT-DLP BASE OPTIONS ───────────────────── #

def ytdlp_opts(extra: dict = None):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "cookiefile": get_cookie_file(),
    }
    if extra:
        opts.update(extra)
    return opts

# ───────────────────── UTIL FUNCTIONS ───────────────────── #

async def shell(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    if err:
        return err.decode()
    return out.decode()

async def check_file_size(url: str):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--cookies", get_cookie_file(),
        "-J",
        url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        log.error(err.decode())
        return None

    data = json.loads(out.decode())
    size = sum(f.get("filesize", 0) for f in data.get("formats", []))
    return size

# ───────────────────── YOUTUBE API ───────────────────── #

class YouTubeAPI:
    BASE = "https://www.youtube.com/watch?v="
    PLAYLIST = "https://youtube.com/playlist?list="
    REGEX = r"(youtube\.com|youtu\.be)"

    # ───────── URL CHECK ───────── #

    async def exists(self, link: str):
        return bool(re.search(self.REGEX, link))

    async def url(self, message: Message) -> Union[str, None]:
        msgs = [message]
        if message.reply_to_message:
            msgs.append(message.reply_to_message)

        for msg in msgs:
            if msg.entities:
                for e in msg.entities:
                    if e.type == MessageEntityType.URL:
                        text = msg.text or msg.caption
                        return text[e.offset : e.offset + e.length]
        return None

    # ───────── VIDEO INFO ───────── #

    async def details(self, link: str):
        if "&" in link:
            link = link.split("&")[0]

        search = VideosSearch(link, limit=1)
        r = (await search.next())["result"][0]

        duration_sec = int(time_to_seconds(r["duration"])) if r["duration"] else 0

        return (
            r["title"],
            r["duration"],
            duration_sec,
            r["thumbnails"][0]["url"].split("?")[0],
            r["id"],
        )

    # ───────── STREAM URL ───────── #

    async def stream(self, link: str):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", get_cookie_file(),
            "-f", "best[height<=720]",
            "-g",
            link,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        out, err = await proc.communicate()
        if out:
            return out.decode().strip(), False
        return None, err.decode()

    # ───────── DOWNLOAD ───────── #

    async def download(
        self,
        link: str,
        video: bool = False,
        audio: bool = False,
        format_id: str = None,
        title: str = None,
    ):
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl = yt_dlp.YoutubeDL(ytdlp_opts({
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
            }))
            info = ydl.extract_info(link, download=True)
            return f"downloads/{info['id']}.{info['ext']}"

        def video_dl():
            ydl = yt_dlp.YoutubeDL(ytdlp_opts({
                "format": "bestvideo[height<=720]+bestaudio",
                "merge_output_format": "mp4",
                "outtmpl": "downloads/%(id)s.%(ext)s",
            }))
            info = ydl.extract_info(link, download=True)
            return f"downloads/{info['id']}.mp4"

        if video:
            if await is_on_off(1):
                path = await loop.run_in_executor(None, video_dl)
                return path, True

            stream, err = await self.stream(link)
            if stream:
                return stream, False

            size = await check_file_size(link)
            if not size or size > 250 * 1024 * 1024:
                return None, False

            path = await loop.run_in_executor(None, video_dl)
            return path, True

        path = await loop.run_in_executor(None, audio_dl)
        return path, True

