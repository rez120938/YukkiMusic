#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import asyncio
import sys
import traceback
from datetime import datetime
from functools import wraps

from pyrogram import Client, StopPropagation
from pyrogram.errors import (
    FloodWait,
    MessageNotModified,
    MessageIdInvalid,
    ChatSendMediaForbidden,
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
)
from pyrogram.handlers import MessageHandler
import config

from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.clients = []
        self.handlers = []

    def add(self, *args, **kwargs):
        """ᴀᴅᴅ ᴀ ɴᴇᴡ ᴄʟɪᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ."""
        self.clients.append(Client(*args, **kwargs))

    async def _start(self, client, index):
        LOGGER(__name__).info(f"ꜱᴛᴀʀᴛɪɴɢ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴄʟɪᴇɴᴛ {index}")
        try:
            await client.start()
            assistants.append(index)
            try:
                await client.send_message(config.LOG_GROUP_ID, "Assistant Started")
            except ChatWriteForbidden:
                try:
                    await client.join_chat(config.LOG_GROUP_ID)
                    await client.send_message(config.LOG_GROUP_ID, "Assistant Started")
                except Exception:
                    LOGGER(__name__).error(
                        f"ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ {index} ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇɴᴅ ᴍᴇꜱꜱᴀɢᴇ ɪɴ ʟᴏɢ ɢʀᴏᴜᴘ. "
                        f"ᴇɴꜱᴜʀᴇ ᴛʜᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ ɪꜱ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ."
                    )
                    sys.exit(1)

            get_me = await client.get_me()
            client.username = get_me.username
            client.id = get_me.id
            client.mention = get_me.mention
            assistantids.append(get_me.id)
            client.name = f"{get_me.first_name} {get_me.last_name or ''}".strip()

            # Add stored handlers to the client
            for handler, group in self.handlers:
                client.add_handler(handler, group)

        except Exception as e:
            LOGGER(__name__).error(
                f"ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ {index} ꜰᴀɪʟᴇᴅ ᴡɪᴛʜ ᴇʀʀᴏʀ: {str(e)}. ᴇxɪᴛɪɴɢ..."
            )
            sys.exit(1)

    async def start(self):
        """ꜱᴛᴀʀᴛ ᴀʟʟ ᴄʟɪᴇɴᴛꜱ."""
        tasks = [self._start(client, i) for i, client in enumerate(self.clients, start=1)]
        await asyncio.gather(*tasks)

    async def stop(self):
        """ɢʀᴀᴄᴇꜰᴜʟʟʏ ꜱᴛᴏᴘ ᴀʟʟ ᴄʟɪᴇɴᴛꜱ."""
        tasks = [client.stop() for client in self.clients]
        await asyncio.gather(*tasks)

    def on_message(self, filters=None, group=0): # on_message decirator for future Userbot Plugins
        """ᴅᴇᴄᴏʀᴀᴛᴏʀ ꜰᴏʀ ʜᴀɴᴅʟɪɴɢ ᴍᴇꜱꜱᴀɢᴇꜱ ᴡɪᴛʜ ᴇʀʀᴏʀ ʜᴀɴᴅʟɪɴɢ."""
        def decorator(func):
            @wraps(func)
            async def wrapper(client, message):
                try:
                    await func(client, message)
                except FloodWait as e:
                    LOGGER(__name__).warning(f"FloodWait: Sleeping for {e.value} seconds.")
                    await asyncio.sleep(e.value)
                except (
                    ChatWriteForbidden,
                    ChatSendMediaForbidden,
                    ChatSendPhotosForbidden,
                    MessageNotModified,
                    MessageIdInvalid,
                ):
                    pass
                except StopPropagation:
                    raise
                except Exception as e:
                    # Detailed error logging
                    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user_id = message.from_user.id if message.from_user else "Unknown"
                    chat_id = message.chat.id if message.chat else "Unknown"
                    chat_username = f"@{message.chat.username}" if message.chat.username else "Private Group"
                    command = (
                        " ".join(message.command)
                        if hasattr(message, "command")
                        else message.text
                    )
                    error_trace = traceback.format_exc()
                    error_message = (
                        f"**ᴇʀʀᴏʀ:** {type(e).__name__}\n"
                        f"**ᴅᴀᴛᴇ:** {date_time}\n"
                        f"**ᴄʜᴀᴛ ɪᴅ:** {chat_id}\n"
                        f"**ᴄʜᴀᴛ ᴜꜱᴇʀɴᴀᴍᴇ:** {chat_username}\n"
                        f"**ᴜꜱᴇʀ ɪᴅ:** {user_id}\n"
                        f"**ᴄᴏᴍᴍᴀɴᴅ/ᴛᴇxᴛ:** {command}\n"
                        f"**ᴛʀᴀᴄᴇʙᴀᴄᴋ:**\n{error_trace}"
                    )
                    await client.send_message(config.LOG_GROUP_ID, error_message)
                    try:
                        await client.send_message(config.OWNER_ID[0], error_message)
                    except Exception:
                        pass

            handler = MessageHandler(wrapper, filters)
            self.handlers.append((handler, group))
            return func

        return decorator
