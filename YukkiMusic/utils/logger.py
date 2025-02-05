#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import is_on_off


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "Private Group"

        logger_text = f"""
**{app.mention} ᴘʟᴀʏ ʟᴏɢ**

**ᴄʜᴀᴛ ɪᴅ:** `{message.chat.id}`
**ᴄʜᴀᴛ ɴᴀᴍᴇ:** {message.chat.title}
**ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ:** {chatusername}

**ᴜꜱᴇʀ ɪᴅ:** `{message.from_user.id}`
**ɴᴀᴍᴇ:** {message.from_user.mention}
**ᴜꜱᴇʀɴᴀᴍᴇ:** @{message.from_user.username}

**Qᴜᴇʀʏ:** {message.text.split(None, 1)[1]}
**ꜱᴛʀᴇᴀᴍ ᴛʏᴘᴇ:** {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass
        return
