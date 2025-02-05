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

import speedtest

from strings import command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ...")
        test.download()
        m = m.edit("⇆ ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ...")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ ꜱʜᴀʀɪɴɢ ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ʀᴇꜱᴜʟᴛꜱ")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(command("SPEEDTEST_COMMAND") & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**ꜱᴘᴇᴇᴅᴛᴇꜱᴛ ʀᴇꜱᴜʟᴛꜱ**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**ɪꜱᴘ:** {result['client']['isp']}
**ᴄᴏᴜɴᴛʀʏ:** {result['client']['country']}
  
<u>**ꜱᴇʀᴠᴇʀ:**</u>
**ɴᴀᴍᴇ:** {result['server']['name']}
**ᴄᴏᴜɴᴛʀʏ:** {result['server']['country']}, {result['server']['cc']}
**ꜱᴘᴏɴꜱᴏʀ:** {result['server']['sponsor']}
**ʟᴀᴛᴇɴᴄʏ:** {result['server']['latency']}  
**ᴘɪɴɢ:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
