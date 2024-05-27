from pyrogram import Client, filters
from pyrogram.types import Message
from config import BANNED_USERS
from LOVEMUSIC import app
from LOVEMUSIC.core.call import LOVE
from LOVEMUSIC.utils.database import is_muted, mute_on, mute_off
from LOVEMUSIC.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["vcmute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def mute_admin(client, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏꜰ ᴄᴏᴍᴍᴀɴᴅ.")
    if await is_muted(chat_id):
        return await message.reply_text(
            "➻ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴍᴜᴛᴇᴅ", disable_web_page_preview=True
        )
    await mute_on(chat_id)
    await LOVE.mute_stream(chat_id)
    await message.reply_text(
        "➻ ᴍᴜsɪᴄ ɪs ᴍᴜᴛᴇᴅ ʙʏ {}!".format(message.from_user.mention),
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(["vcunmute"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unmute_admin(client: Client, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏꜰ ᴄᴏᴍᴍᴀɴᴅ.")
    if not await is_muted(chat_id):
        return await message.reply_text(
            "➻ ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴜɴᴍᴜᴛᴇᴅ", disable_web_page_preview=True
        )
    await mute_off(chat_id)
    await LOVE.unmute_stream(chat_id)
    await message.reply_text(
        "➻ ᴍᴜsɪᴄ ɪs ᴜɴᴍᴜᴛᴇᴅ ʙʏ {}!".format(message.from_user.mention),
        disable_web_page_preview=True,
    )
