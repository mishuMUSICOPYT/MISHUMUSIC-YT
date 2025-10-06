import asyncio
import random

from pyrogram import app filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import UserNotParticipant

from RessoMusic import app
from RessoMusic.utils.branded_ban import admin_filter

SPAM_CHATS = []
spam_chats = []

# --------------------------- TAG ALL USERS --------------------------- #
@app.on_message(
    filters.command(["all", "mention", "mentionall"], prefixes=["/", "@", ".", "#"])
    & admin_filter
)
async def tag_all_users(_, message):
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text("Use /all with a message or reply to tag everyone.")
    if replied:
        SPAM_CHATS.append(message.chat.id)
        usernum, usertxt = 0, ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n➥ [{m.user.first_name}](tg://user?id={m.user.id})"
            if usernum == 5:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum, usertxt = 0, ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except:
            pass
    else:
        text = message.text.split(None, 1)[1]
        SPAM_CHATS.append(message.chat.id)
        usernum, usertxt = 0, ""
        async for m in app.get_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n➥ [{m.user.first_name}](tg://user?id={m.user.id})"
            if usernum == 5:
                await app.send_message(
                    message.chat.id,
                    f"{text}\n{usertxt}\n\n ➜ Ongoing tagging » /cancel",
                )
                await asyncio.sleep(2)
                usernum, usertxt = 0, ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except:
            pass

# --------------------------- STOP MENTION --------------------------- #
@app.on_message(
    filters.command(
        ["stopmention", "offall", "cancel", "allstop", "stopall",
         "cancelmention", "offmention", "mentionoff", "alloff",
         "cancelall", "allcancel"],
        prefixes=["/", "@", "#"],
    ) & admin_filter
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except:
            pass
        return await message.reply_text("✅ Tagging process stopped successfully!")
    else:
        return await message.reply_text("No tagging process is running!")

# --------------------------- TAG ALL WITH RANDOM --------------------------- #
@app.on_message(filters.command(["tagall"], prefixes=["/", "@", ".", "#"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("This command works only in groups!")

    # Admin check
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        return await message.reply("Only admins can use this command!")
    else:
        if participant.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return await message.reply("You must be an admin to use this command!")

    if message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
    else:
        return await message.reply("Use /tagall with a message or reply to one.")

    if chat_id in spam_chats:
        return await message.reply("Tagging already in progress...")
    spam_chats.append(chat_id)
