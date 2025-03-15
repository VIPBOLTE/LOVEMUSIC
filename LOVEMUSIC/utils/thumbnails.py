import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import YOUTUBE_IMG_URL

async def download_image(url, path):
    """Downloads an image from the URL and saves it."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(path, mode="wb") as f:
                        await f.write(await resp.read())
                    return path
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None  

def truncate(text):
    """Truncates title text into two lines."""
    words = text.split(" ")
    text1, text2 = "", ""
    for word in words:
        if len(text1) + len(word) < 30:
            text1 += " " + word
        elif len(text2) + len(word) < 30:
            text2 += " " + word
    return text1.strip(), text2.strip()

async def get_thumb(videoid, has_spoiler=False):
    """Fetches video thumbnail and generates an overlay image."""
    cached_path = f"cache/{videoid}_v4.png"
    if os.path.isfile(cached_path):
        return cached_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)

    try:
        response = await results.next()
        result = response["result"][0] if response and "result" in response and response["result"] else None
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return YOUTUBE_IMG_URL  

    if not result:
        print("Error: No results found.")
        return YOUTUBE_IMG_URL  

    title = re.sub("\W+", " ", result.get("title", "Unknown Title")).title()
    duration = result.get("duration")
    thumbnail_url = result.get("thumbnails", [{}])[0].get("url", "").split("?")[0]
    views = result.get("viewCount", {}).get("short", "Unknown Views")
    channel = result.get("channel", {}).get("name", "Unknown Channel")

    is_live = duration is None
    duration_text = "🔴 LIVE" if is_live else duration

    thumbnail_path = f"cache/thumb{videoid}.png"
    downloaded_path = await download_image(thumbnail_url, thumbnail_path)
    if not downloaded_path:  
        downloaded_path = await download_image(YOUTUBE_IMG_URL, thumbnail_path)

    try:
        youtube = Image.open(downloaded_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return YOUTUBE_IMG_URL

    # Ensure the image is square
    width, height = youtube.size
    if width != height:
        new_size = min(width, height)
        left = (width - new_size) / 2
        top = (height - new_size) / 2
        right = (width + new_size) / 2
        bottom = (height + new_size) / 2
        youtube = youtube.crop((left, top, right, bottom))

    blurred_background = youtube.convert("RGBA").filter(ImageFilter.GaussianBlur(20))
    blurred_background = ImageEnhance.Brightness(blurred_background).enhance(0.6)

    # Create circular HD thumbnail with a thick border
    circle_size = 400
    hd_thumbnail = youtube.resize((circle_size, circle_size), Image.LANCZOS)

    # Create circular mask
    circle_mask = Image.new("L", (circle_size, circle_size), 0)
    draw_mask = ImageDraw.Draw(circle_mask)
    draw_mask.ellipse((0, 0, circle_size, circle_size), fill=255)
    hd_thumbnail.putalpha(circle_mask)

    # Create border
    border_thickness = 20
    border_size = circle_size + (border_thickness * 2)
    border_circle = Image.new("RGBA", (border_size, border_size), (255, 255, 255, 255))
    border_mask = Image.new("L", (border_size, border_size), 0)
    border_draw = ImageDraw.Draw(border_mask)
    border_draw.ellipse((0, 0, border_size, border_size), fill=255)
    border_circle.putalpha(border_mask)

    # Drawing Logic
    draw = ImageDraw.Draw(blurred_background)

    try:
        font = ImageFont.truetype("LOVEMUSIC/assets/font.ttf", 30)
        title_font = ImageFont.truetype("LOVEMUSIC/assets/font3.ttf", 45)
        info_font = ImageFont.truetype("LOVEMUSIC/assets/font.ttf", 25)
    except Exception as e:
        print(f"Error loading fonts: {e}")
        return YOUTUBE_IMG_URL

    # Title Text
    text_x = 565
    title1, title2 = truncate(title)
    draw.text((text_x, 180), title1, fill=(255, 255, 255), font=title_font)
    draw.text((text_x, 230), title2, fill=(255, 255, 255), font=title_font)

    # Channel and View Count
    draw.text((text_x, 320), f"{channel} | {views}", fill=(255, 255, 255), font=info_font)

    # Progress Line
    progress_line_start_x = text_x
    progress_line_end_x = text_x + 580
    draw.line([progress_line_start_x, 380, progress_line_start_x + 348, 380], fill="red", width=9)
    draw.line([progress_line_start_x + 348, 380, progress_line_end_x, 380], fill="white", width=8)
    draw.ellipse([(progress_line_start_x + 348 - 5, 380 - 5), 
                  (progress_line_start_x + 348 + 5, 380 + 5)], fill="red")

    # Duration Text
    draw.text((text_x, 400), "00:00", (255, 255, 255), font=info_font)
    draw.text((1080, 400), duration_text, (255, 255, 255), font=info_font)

    # Overlay Play Button
    try:
        play_icons = Image.open("LOVEMUSIC/assets/play_icons.png").resize((580, 62))
        blurred_background.paste(play_icons, (text_x, 450), play_icons)
    except Exception as e:
        print(f"Error opening play_icons.png: {e}")

    # If has_spoiler is True, add a spoiler overlay
    if has_spoiler:
        # Adding a red "SPOILER" text
        spoiler_text = "SPOILER ALERT"
        spoiler_font = ImageFont.truetype("LOVEMUSIC/assets/font.ttf", 50)
        draw.text((text_x + 150, 300), spoiler_text, fill=(255, 0, 0), font=spoiler_font)

    # Final Image Composition
    hd_position = (60, 140)
    blurred_background.paste(border_circle, hd_position, border_circle)
    blurred_background.paste(hd_thumbnail, (hd_position[0] + border_thickness, hd_position[1] + border_thickness), hd_thumbnail)

    try:
        os.remove(thumbnail_path)
    except:
        pass

    blurred_background.save(cached_path)
    return cached_path
