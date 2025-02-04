from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import json
import os
from datetime import datetime
import config
from strings import command
from YukkiMusic import app
from config import BANNED_USERS
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import (
    get_playlist_names,
    get_playlist,
    delete_playlist,
    get_userss,
    is_banned_user,
    authuserdb,
    delete_served_user,
    remove_sudo,
)


TEXT = f"""
🔒 **Privacy Policy for {app.mention} !**

𝐘𝐨𝐮𝐫 𝐩𝐫𝐢𝐯𝐚𝐜𝐲 𝐢𝐬 𝐢𝐦𝐩𝐨𝐫𝐭𝐚𝐧𝐭 𝐭𝐨 𝐮𝐬. 𝐓𝐨 𝐥𝐞𝐚𝐫𝐧 𝐦𝐨𝐫𝐞 𝐚𝐛𝐨𝐮𝐭 𝐡𝐨𝐰 𝐰𝐞 𝐜𝐨𝐥𝐥𝐞𝐜𝐭, 𝐮𝐬𝐞, 𝐚𝐧𝐝 𝐩𝐫𝐨𝐭𝐞𝐜𝐭 𝐲𝐨𝐮𝐫 𝐝𝐚𝐭𝐚.   
𝐈𝐟 𝐲𝐨𝐮 𝐡𝐚𝐯𝐞 𝐚𝐧𝐲 𝐪𝐮𝐞𝐬𝐭𝐢𝐨𝐧𝐬 𝐨𝐫 𝐜𝐨𝐧𝐜𝐞𝐫𝐧𝐬, 𝐟𝐞𝐞𝐥 𝐟𝐫𝐞𝐞 𝐭𝐨 𝐫𝐞𝐚𝐜𝐡 𝐨𝐮𝐭 𝐭𝐨 𝐨𝐮𝐫 [Support Team]({config.SUPPORT_GROUP}).
"""


PRIVACY_SECTIONS = {
    "collect": """
**What Information We Collect**

• 𝐁𝐚𝐬𝐢𝐜 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐮𝐬𝐞𝐫 𝐝𝐚𝐭𝐚 (𝐈𝐃, 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞) 
• 𝐂𝐡𝐚𝐭/𝐆𝐫𝐨𝐮𝐩 𝐈𝐃𝐬 𝐰𝐡𝐞𝐫𝐞 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐢𝐬 𝐮𝐬𝐞𝐝 
• 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐮𝐬𝐚𝐠𝐞 𝐚𝐧𝐝 𝐢𝐧𝐭𝐞𝐫𝐚𝐜𝐭𝐢𝐨𝐧𝐬 
• 𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭𝐬 𝐚𝐧𝐝 𝐦𝐮𝐬𝐢𝐜 𝐩𝐫𝐞𝐟𝐞𝐫𝐞𝐧𝐜𝐞𝐬 
• 𝐕𝐨𝐢𝐜𝐞 𝐜𝐡𝐚𝐭 𝐩𝐚𝐫𝐭𝐢𝐜𝐢𝐩𝐚𝐭𝐢𝐨𝐧 𝐝𝐚𝐭𝐚 
• 𝐔𝐬𝐞𝐫 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐚𝐧𝐝 𝐜𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧𝐬
""",
    "why": """
**Why We Collect It**

• 𝐓𝐨 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐦𝐮𝐬𝐢𝐜 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐬𝐞𝐫𝐯𝐢𝐜𝐞𝐬 
• 𝐓𝐨 𝐦𝐚𝐢𝐧𝐭𝐚𝐢𝐧 𝐮𝐬𝐞𝐫 𝐩𝐥𝐚𝐲𝐥𝐢𝐬𝐭𝐬 
• 𝐓𝐨 𝐩𝐫𝐨𝐜𝐞𝐬𝐬 𝐯𝐨𝐢𝐜𝐞 𝐜𝐡𝐚𝐭 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬 
• 𝐓𝐨 𝐦𝐚𝐧𝐚𝐠𝐞 𝐮𝐬𝐞𝐫 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬 
• 𝐓𝐨 𝐢𝐦𝐩𝐫𝐨𝐯𝐞 𝐛𝐨𝐭 𝐟𝐞𝐚𝐭𝐮𝐫𝐞𝐬 
• 𝐓𝐨 𝐩𝐫𝐞𝐯𝐞𝐧𝐭 𝐚𝐛𝐮𝐬𝐞 𝐚𝐧𝐝 𝐬𝐩𝐚𝐦
""",
    "do": """
**What We Do**

• 𝐒𝐭𝐨𝐫𝐞 𝐝𝐚𝐭𝐚 𝐬𝐞𝐜𝐮𝐫𝐞𝐥𝐲 𝐢𝐧 𝐞𝐧𝐜𝐫𝐲𝐩𝐭𝐞𝐝 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞𝐬 
• 𝐏𝐫𝐨𝐜𝐞𝐬𝐬 𝐦𝐮𝐬𝐢𝐜 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬 𝐚𝐧𝐝 𝐬𝐭𝐫𝐞𝐚𝐦𝐬 
• 𝐌𝐚𝐢𝐧𝐭𝐚𝐢𝐧 𝐮𝐬𝐞𝐫 𝐩𝐫𝐞𝐟𝐞𝐫𝐞𝐧𝐜𝐞𝐬 
• 𝐌𝐨𝐧𝐢𝐭𝐨𝐫 𝐟𝐨𝐫 𝐩𝐫𝐨𝐩𝐞𝐫 𝐟𝐮𝐧𝐜𝐭𝐢𝐨𝐧𝐚𝐥𝐢𝐭𝐲 
• 𝐃𝐞𝐥𝐞𝐭𝐞 𝐭𝐞𝐦𝐩𝐨𝐫𝐚𝐫𝐲 𝐟𝐢𝐥𝐞𝐬 𝐚𝐟𝐭𝐞𝐫 𝐮𝐬𝐞 
• 𝐈𝐦𝐩𝐥𝐞𝐦𝐞𝐧𝐭 𝐬𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐦𝐞𝐚𝐬𝐮𝐫𝐞𝐬
""",
    "donot": """
**What We Don't Do**

• 𝐒𝐡𝐚𝐫𝐞 𝐲𝐨𝐮𝐫 𝐝𝐚𝐭𝐚 𝐰𝐢𝐭𝐡 𝐭𝐡𝐢𝐫𝐝 𝐩𝐚𝐫𝐭𝐢𝐞𝐬 
• 𝐒𝐭𝐨𝐫𝐞 𝐮𝐧𝐧𝐞𝐜𝐞𝐬𝐬𝐚𝐫𝐲 𝐩𝐞𝐫𝐬𝐨𝐧𝐚𝐥 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧 
• 𝐊𝐞𝐞𝐩 𝐝𝐚𝐭𝐚 𝐥𝐨𝐧𝐠𝐞𝐫 𝐭𝐡𝐚𝐧 𝐧𝐞𝐞𝐝𝐞𝐝 
• 𝐔𝐬𝐞 𝐝𝐚𝐭𝐚 𝐟𝐨𝐫 𝐦𝐚𝐫𝐤𝐞𝐭𝐢𝐧𝐠 
• 𝐓𝐫𝐚𝐜𝐤 𝐮𝐬𝐞𝐫𝐬 𝐚𝐜𝐫𝐨𝐬𝐬 𝐩𝐥𝐚𝐭𝐟𝐨𝐫𝐦𝐬 
• 𝐒𝐞𝐥𝐥 𝐚𝐧𝐲 𝐮𝐬𝐞𝐫 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
""",
    "rights": """
**Your Rights**

• 𝐀𝐜𝐜𝐞𝐬𝐬 𝐲𝐨𝐮𝐫 𝐬𝐭𝐨𝐫𝐞𝐝 𝐝𝐚𝐭𝐚 
• 𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐝𝐚𝐭𝐚 𝐝𝐞𝐥𝐞𝐭𝐢𝐨𝐧 
• 𝐌𝐨𝐝𝐢𝐟𝐲 𝐲𝐨𝐮𝐫 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 
• 𝐎𝐩𝐭-𝐨𝐮𝐭 𝐨𝐟 𝐝𝐚𝐭𝐚 𝐜𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧 
• 𝐑𝐞𝐩𝐨𝐫𝐭 𝐩𝐫𝐢𝐯𝐚𝐜𝐲 𝐜𝐨𝐧𝐜𝐞𝐫𝐧𝐬 
• 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐬𝐮𝐩𝐩𝐨𝐫𝐭 𝐟𝐨𝐫 𝐡𝐞𝐥𝐩
""",
}


async def find_chat_ids_by_auth_user_id(auth_user_id):
    chat_ids = []
    async for document in authuserdb.find():
        for note_key, note_data in document.get("notes", {}).items():
            if note_data.get("auth_user_id") == auth_user_id:
                chat_ids.append(document["chat_id"])
    return chat_ids


async def delete_auth_user_data(auth_user_id):
    async for document in authuserdb.find():
        chat_id = document["chat_id"]
        notes = document.get("notes", {})
        keys_to_remove = [
            key
            for key, value in notes.items()
            if value.get("auth_user_id") == auth_user_id
        ]
        for key in keys_to_remove:
            notes.pop(key)
        if keys_to_remove:
            await authuserdb.update_one(
                {"chat_id": chat_id}, {"$set": {"notes": notes}}
            )


@app.on_message(command("PRIVACY_COMMAND") & ~BANNED_USERS)
async def privacy_menu(client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ", callback_data="show_privacy_sections"
                )
            ],
            [
                InlineKeyboardButton("ʀᴇᴛʀɪᴇᴠᴇ ᴅᴀᴛᴀ", callback_data="retrieve_data"),
                InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴅᴀᴛᴀ", callback_data="delete_data"),
            ],
            [InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")],
        ]
    )
    await message.reply_text(TEXT, reply_markup=keyboard, disable_web_page_preview=True)


@app.on_callback_query(filters.regex("show_privacy_sections") & ~BANNED_USERS)
async def show_privacy_sections(client, callback_query):
    """ꜱʜᴏᴡ ᴅᴇᴛᴀɪʟᴇᴅ ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ ꜱᴇᴄᴛɪᴏɴꜱ"""
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("What We Collect", callback_data="privacy_collect")],
            [InlineKeyboardButton("Why We Collect", callback_data="privacy_why")],
            [InlineKeyboardButton("What We Do", callback_data="privacy_do")],
            [InlineKeyboardButton("What We Don't Do", callback_data="privacy_donot")],
            [InlineKeyboardButton("Your Rights", callback_data="privacy_rights")],
            [
                InlineKeyboardButton("Back", callback_data="privacy_back"),
                InlineKeyboardButton("Close", callback_data="close"),
            ],
        ]
    )
    await callback_query.edit_message_text(
        f"{TEXT}\n\nꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇᴄᴛɪᴏɴ ᴛᴏ ʟᴇᴀʀɴ ᴍᴏʀᴇ:",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


@app.on_callback_query(filters.regex("privacy_") & ~BANNED_USERS)
async def privacy_section_callback(client, callback_query):
    """ʜᴀɴᴅʟᴇ ᴘʀɪᴠᴀᴄʏ ꜱᴇᴄᴛɪᴏɴ ᴄᴀʟʟʙᴀᴄᴋꜱ"""
    section = callback_query.data.split("_")[1]

    if section == "back":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ", callback_data="show_privacy_sections"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ʀᴇᴛʀɪᴇᴠᴇ ᴅᴀᴛᴀ", callback_data="retrieve_data"
                    ),
                    InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ ᴅᴀᴛᴀ", callback_data="delete_data"),
                ],
                [InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")],
            ]
        )
        return await callback_query.edit_message_text(
            TEXT, reply_markup=keyboard, disable_web_page_preview=True
        )

    if section in PRIVACY_SECTIONS:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="show_privacy_sections"),
                    InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"),
                ],
            ]
        )
        await callback_query.edit_message_text(
            PRIVACY_SECTIONS[section], reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("retrieve_data"))
async def export_user_data(_, cq):
    m = await cq.message.edit("Please wait..")
    user_id = cq.from_user.id
    user_data = {
        "ᴜꜱᴇʀ_ɪᴅ": user_id,
        "ᴇxᴘᴏʀᴛ_ᴅᴀᴛᴇ": datetime.now().isoformat(),
        "ʙᴀꜱɪᴄ_ɪɴꜰᴏ": {
            "ᴜꜱᴇʀ_ɪᴅ": user_id,
            "ᴜꜱᴇʀɴᴀᴍᴇ": cq.from_user.username,
            "ꜰɪʀꜱᴛ_ɴᴀᴍᴇ": cq.from_user.first_name,
            "ʟᴀꜱᴛ_ɴᴀᴍᴇ": cq.from_user.last_name,
        },
        "ᴘʟᴀʏʟɪꜱᴛꜱ": {},
        "ᴀᴜᴛʜᴇᴅ_ɪɴ": await find_chat_ids_by_auth_user_id(user_id),
        "ʙᴀɴ_ꜱᴛᴀᴛᴜꜱ": await is_banned_user(user_id),
        "ꜱᴜᴅᴏ_ꜱᴛᴀᴛᴜꜱ": user_id in SUDOERS,
        "ᴜꜱᴇʀ_ꜱᴛᴀᴛꜱ": await get_userss(user_id),
    }
    try:
        playlist_names = await get_playlist_names(user_id)
        for name in playlist_names:
            playlist = await get_playlist(user_id, name)
            if playlist:
                user_data["playlists"][name] = playlist
    except Exception as e:
        pass
    user_data = {
        k: (
            {sk: sv for sk, sv in v.items() if sv is not None}
            if isinstance(v, dict)
            else v
        )
        for k, v in user_data.items()
        if v is not None
    }

    file_path = os.path.join("cache", f"user_data_{user_id}.json")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        return await m.edit(
            f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴄʀᴇᴀᴛɪɴɢ ᴅᴀᴛᴀ ꜰɪʟᴇ: {str(e)}", show_alert=True
        )

    try:
        await cq.message.reply_document(
            document=file_path,
            caption=(
                "🔒 ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ᴜꜱᴇʀ ᴅᴀᴛᴀ ᴇxᴘᴏʀᴛ ꜰʀᴏᴍ ʀᴇᴢ.\n\n"
                "⚠️ ᴛʜɪꜱ ꜰɪʟᴇ ᴄᴏɴᴛᴀɪɴꜱ ʏᴏᴜʀ ᴘᴇʀꜱᴏɴᴀʟ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ. "
                "ᴘʟᴇᴀꜱᴇ ʜᴀɴᴅʟᴇ ɪᴛ ᴄᴀʀᴇꜰᴜʟʟʏ ᴀɴᴅ ᴅᴏ ɴᴏᴛ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ᴏᴛʜᴇʀꜱ.\n\n"
                "📊 ɪɴᴄʟᴜᴅᴇꜱ:\n"
                "- ᴘᴇʀꜱᴏɴᴀʟ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ\n"
                "- ᴘʟᴀʏʟɪꜱᴛꜱ\n"
                "- ᴜꜱᴀɢᴇ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ\n"
                "- ᴀᴜᴛʜᴏʀɪᴢᴀᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ\n"
                "- ʙᴀɴ ꜱᴛᴀᴛᴜꜱ\n"
                "- ꜱᴜᴅᴏ ᴘʀɪᴠɪʟᴇɢᴇꜱ\n"
            ),
            file_name=f"data_{user_id}_.json",
        )
    except Exception as e:
        await m.edit(
            f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴄʀᴇᴀᴛɪɴɢ ᴅᴀᴛᴀ ꜰɪʟᴇ: {str(e)}", show_alert=True
        )
    finally:
        try:
            await cq.message.delete()
            os.remove(file_path)
        except Exception:
            pass


@app.on_callback_query(filters.regex("delete_data"))
async def retrieve_data(_, cq):
    await cq.message.edit(
        "ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴅᴀᴛᴀ?",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ʏᴇꜱ", callback_data="confirm_delete_data")],
                [InlineKeyboardButton("ɴᴏ", callback_data="privacy_back")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("confirm_delete_data"))
async def delete_user_data(_, cq):
    await cq.answer("ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...", show_alert=True)

    user_id = cq.from_user.id

    try:
        _playlist = await get_playlist_names(user_id)
        for x in _playlist:
            await delete_playlist(user_id, x)
    except Exception:
        pass

    await delete_auth_user_data(user_id)
    await delete_served_user(user_id)

    if user_id in SUDOERS:
        SUDOERS.remove(user_id)
    try:
        await remove_sudo(user_id)
    except Exception:
        pass

    await delete_userss(user_id)
    await cq.edit_message_text("ʏᴏᴜʀ ᴅᴀᴛᴀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.")
