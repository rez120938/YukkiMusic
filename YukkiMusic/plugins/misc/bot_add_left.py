#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import delete_served_chat, get_assistant, is_on_off


@app.on_message(filters.new_chat_members)
async def on_bot_added(_, message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)
        chat = message.chat
        for members in message.new_chat_members:
            if members.id == app.id:
                count = await app.get_chat_members_count(chat.id)
                username = (
                    message.chat.username if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
                )
                msg = (
                    f"**ᴍᴜꜱɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ɴᴇᴡ ɢʀᴏᴜᴘ #New_Group**\n\n"
                    f"**ᴄʜᴀᴛ ɴᴀᴍᴇ:** {message.chat.title}\n"
                    f"**ᴄʜᴀᴛ ɪᴅ:** {message.chat.id}\n"
                    f"**ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ:** @{username}\n"
                    f"**ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ ᴄᴏᴜɴᴛ:** {count}\n"
                    f"**ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention}"
                )
                await app.send_message(
                    LOG_GROUP_ID,
                    text=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=f"ᴀᴅᴅᴇᴅ ʙʏ: {message.from_user.first_name}",
                                    user_id=message.from_user.id,
                                )
                            ]
                        ]
                    ),
                )
                if message.chat.username:
                    await userbot.join_chat(message.chat.username)
    except Exception:
        pass


@app.on_message(filters.left_chat_member)
async def on_bot_kicked(_, message: Message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == app.id:
            remove_by = (
                message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
            )
            chat_id = message.chat.id
            left = (
                f"ʙᴏᴛ ᴡᴀꜱ ʀᴇᴍᴏᴠᴇᴅ ɪɴ {title} #Left_group\n"
                f"**ᴄʜᴀᴛ ɴᴀᴍᴇ**: {title}\n"
                f"**ᴄʜᴀᴛ ɪᴅ**: {chat_id}\n"
                f"**ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ**: {username}\n"
                f"**ʀᴇᴍᴏᴠᴇᴅ ʙʏ**: {remove_by}"
            )

            await app.send_message(
                LOG_GROUP_ID,
                text=left,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"ʀᴇᴍᴏᴠᴇᴅ ʙʏ: {message.from_user.first_name}",
                                user_id=message.from_user.id,
                            )
                        ]
                    ]
                ),
            )
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        pass
