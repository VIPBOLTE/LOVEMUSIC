import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PRIVATE_BOT_MODE, SUPPORT_CHAT
from strings import get_string
from LOVEMUSIC import YouTube, app
from LOVEMUSIC.core.call import _clear_ as clean
from LOVEMUSIC.misc import SUDOERS
from LOVEMUSIC.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_served_private_chat,
)

links = {}


def RadioWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        userbot = await get_assistant(message.chat.id)

        # Ensure userbot is available before proceeding
        if not userbot:
            return await message.reply_text("❌ Assistant bot is not available. Please try again later.")

        _ = get_string(language)
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)

        if not await is_maintenance():
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a>.",
                    disable_web_page_preview=True,
                )

        if PRIVATE_BOT_MODE == str(True) and not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**ᴘʀɪᴠᴀᴛᴇ ᴍᴜsɪᴄ ʙᴏᴛ**\n\nᴏɴʟʏ ғᴏʀ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴄʜᴀᴛs."
            )
            return await app.leave_chat(message.chat.id)

        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass

        url = await YouTube.url(message)
        chat_id = await get_cmode(message.chat.id) if message.command[0][0] == "c" else message.chat.id

        try:
            chat = await app.get_chat(chat_id)
            channel = chat.title if message.command[0][0] == "c" else None
        except:
            return await message.reply_text(_["cplay_4"])

        try:
            is_call_active = (await app.get_chat(chat_id)).is_call_active
            if not is_call_active:
                return await message.reply_text("**» No active video chat found.**")
        except Exception:
            pass

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        if playty != "Everyone" and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id, [])
            if message.from_user.id not in admins:
                return await message.reply_text(_["play_4"])

        video = "v" in message.command[0] or "-v" in message.text
        fplay = message.command[0][-1] == "e" and await is_active_chat(chat_id)

        # Check if userbot is already in chat
        try:
            common_chats = await userbot.get_common_chats(app.username)
            if any(chat.id == message.chat.id for chat in common_chats):
                call_participants_id = [member.user.id async for member in userbot.get_chat_members(chat_id)]
                if await is_active_chat(chat_id) and userbot.id not in call_participants_id:
                    await clean(chat_id)

                return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)
        except Exception as e:
            print(f"Error checking common chats: {e}")

        # Try joining via username
        if message.chat.username:
            try:
                await userbot.join_chat(message.chat.username)
                call_participants_id = [member.user.id async for member in userbot.get_chat_members(chat_id)]
                if await is_active_chat(chat_id) and userbot.id not in call_participants_id:
                    await clean(chat_id)

                return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)
            except Exception as e:
                print(f"Error joining via username: {e}")

        # Fallback: Joining via invite link
        if not await is_active_chat(chat_id):
            userbot_id = userbot.id
            try:
                get = await app.get_chat_member(chat_id, userbot_id)
                if get.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
                    try:
                        await app.unban_chat_member(chat_id, userbot_id)
                    except:
                        return await message.reply_text(_["call_2"].format(userbot.username, userbot_id))
            except UserNotParticipant:
                invitelink = links.get(chat_id) or (message.chat.username or await app.export_chat_invite_link(chat_id))
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")

                myu = await message.reply_text(_["call_5"])
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await myu.edit(_["call_3"].format(type(e).__name__))
                    await asyncio.sleep(1)
                    await myu.edit(_["call_6"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await myu.edit(_["call_3"].format(type(e).__name__))

                links[chat_id] = invitelink
                try:
                    await myu.delete()
                except:
                    pass

        # Ensure userbot is available before proceeding
        userbot = await get_assistant(message.chat.id)
        if not userbot:
            return await message.reply_text("❌ Assistant bot is not available. Please try again later.")

        call_participants_id = [member.user.id async for member in userbot.get_chat_members(chat_id)]
        if await is_active_chat(chat_id) and userbot.id not in call_participants_id:
            await clean(chat_id)

        return await command(client, message, _, chat_id, video, channel, playmode, url, fplay)

    return wrapper
