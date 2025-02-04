#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from os import path
from typing import Union

from yt_dlp import YoutubeDL

from YukkiMusic.utils.formatters import seconds_to_min
from YukkiMusic.utils.decorators import asyncify


class SoundCloud:
    def __init__(self):
        self.opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "format": "best",
            "retries": 3,
            "nooverwrites": False,
            "continuedl": True,
        }

    async def valid(self, link: str) -> bool:
        return "soundcloud" in link

    @asyncify
    def download(self, url: str) -> Union[dict, bool]:
        with YoutubeDL(self.opts):
            try:
                info = d.extract_info(url)
            except Exception:
                return False
            xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
            duration_min = seconds_to_min(info["duration"])
            track_details = {
                "ᴛɪᴛʟᴇ": info["title"],
                "ᴅᴜʀᴀᴛɪᴏɴ_ꜱᴇᴄ": info["duration"],
                "ᴅᴜʀᴀᴛɪᴏɴ_ᴍɪɴ": duration_min,
                "ᴜᴘʟᴏᴀᴅᴇʀ": info["uploader"],
                "ꜰɪʟᴇᴘᴀᴛʜ": xyz,
            }
            return track_details, xyz
