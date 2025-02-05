import asyncio
import json
import os
from datetime import datetime

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure
from pyrogram import filters
from pyrogram.errors import FloodWait

from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from YukkiMusic import app
from YukkiMusic.core.mongo import DB_NAME


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 format
        return super().default(obj)


async def ex_port(db, db_name):
    data = {}
    collections = await db.list_collection_names()

    for collection_name in collections:
        collection = db[collection_name]
        documents = await collection.find().to_list(length=None)
        data[collection_name] = documents

    file_path = os.path.join("cache", f"{db_name}_backup.txt")
    with open(file_path, "w") as backup_file:
        json.dump(data, backup_file, indent=4, cls=CustomJSONEncoder)

    return file_path


async def drop_db(client, db_name):
    await client.drop_database(db_name)


async def edit_or_reply(mystic, text):
    try:
        return await mystic.edit_text(text, disable_web_page_preview=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await mystic.edit_text(text, disable_web_page_preview=True)
    try:
        await mystic.delete()
    except Exception:
        pass
    return await app.send_message(mystic.chat.id, disable_web_page_preview=True)


@app.on_message(filters.command("export") & ~BANNED_USERS)
async def export_database(client, message):
    if message.from_user.id not in OWNER_ID:
        return
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**ᴅᴜᴇ ᴛᴏ ꜱᴏᴍᴇ ᴘʀɪᴠᴀᴄʏ ɪꜱꜱᴜᴇ, ʏᴏᴜ ᴄᴀɴ'ᴛ ɪᴍᴘᴏʀᴛ/ᴇxᴘᴏʀᴛ ᴡʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴜꜱɪɴɢ ʏᴜᴋᴋɪ ᴅᴀᴛᴀʙᴀꜱᴇ\n\n ᴘʟᴇᴀꜱᴇ ꜰɪʟʟ ʏᴏᴜʀ ᴍᴏɴɢᴏ_ᴅʙ_ᴜʀɪ ɪɴ ᴠᴀʀꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇꜱ**"
        )
    mystic = await message.reply_text("ᴇxᴘᴏʀᴛɪɴɢ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅᴀᴛᴀʙᴀꜱᴇ...")
    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    databases = await _mongo_async_.list_database_names()

    for db_name in databases:
        if db_name in ["local", "admin", DB_NAME]:
            continue

        db = _mongo_async_[db_name]
        mystic = await edit_or_reply(
            mystic,
            f"ꜰᴏᴜɴᴅ ᴅᴀᴛᴀ ᴏꜰ {db_name} ᴅᴀᴛᴀʙᴀꜱᴇ. **ᴜᴘʟᴏᴀᴅɪɴɢ** and **ᴅᴇʟᴇᴛɪɴɢ**...",
        )

        file_path = await ex_port(db, db_name)
        try:

            await app.send_document(
                message.chat.id, file_path, caption=f"ᴍᴏɴɢᴏᴅʙ ʙᴀᴄᴋᴜᴘ ᴅᴀᴛᴀ ҒᴏƦ  {db_name}"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        try:
            await drop_db(_mongo_async_, db_name)
        except OperationFailure:
            mystic = await edit_or_reply(
                mystic,
                f"ɪɴ ʏᴏᴜʀ ᴍᴏɴɢᴏᴅʙ ᴅᴇʟᴇᴛɪɴɢ ᴅᴀᴛᴀʙᴀꜱᴇ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ꜱᴏ ɪ ᴄᴀɴ'ᴛ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ {db_name} ᴅᴀᴛᴀʙᴀꜱᴇ",
            )
        try:
            os.remove(file_path)
        except Exception:
            pass

    db = _mongo_async_[DB_NAME]
    mystic = await edit_or_reply(mystic, f"ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...\nᴇxᴘᴏʀᴛɪɴɢ ᴅᴀᴛᴀ ᴏꜰ ʙᴏᴛ")

    async def progress(current, total):
        try:
            await mystic.edit_text(f"ᴜᴘʟᴏᴀᴅɪɴɢ.... {current * 100 / total:.1f}%")
        except FloodWait as e:
            await asyncio.sleep(e.value)

    file_path = await ex_port(db, DB_NAME)
    try:
        await app.send_document(
            message.chat.id,
            file_path,
            caption=f"ᴍᴏɴɢᴏ ʙᴀᴄᴋᴜᴘ ᴏꜰ {app.mention}. ʏᴏᴜ ᴄᴀɴ ɪᴍᴘᴏʀᴛ ᴛʜɪꜱ ɪɴ ᴀ ɴᴇᴡ ᴍᴏɴɢᴏᴅʙ ɪɴꜱᴛᴀɴᴄᴇ ʙʏ ʀᴇᴘʟʏɪɴɢ /import",
            progress=progress,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)

    await mystic.delete()


@app.on_message(filters.command("import") & ~BANNED_USERS)
async def import_database(client, message):
    if message.from_user.id not in OWNER_ID:
        return
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**ᴅᴜᴇ ᴛᴏ ꜱᴏᴍᴇ ᴘʀɪᴠᴀᴄʏ ɪꜱꜱᴜᴇ, ʏᴏᴜ ᴄᴀɴ'ᴛ ɪᴍᴘᴏʀᴛ/ᴇxᴘᴏʀᴛ ᴡʜᴇɴ ʏᴏᴜ ᴀʀᴇ ᴜꜱɪɴɢ ʏᴜᴋᴋɪ ᴅᴀᴛᴀʙᴀꜱᴇ\n\n ᴘʟᴇᴀꜱᴇ ꜰɪʟʟ ʏᴏᴜʀ ᴍᴏɴɢᴏ_ᴅʙ_ᴜʀɪ ɪɴ ᴠᴀʀꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇꜱ**"
        )

    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply_text(
            "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴀɴ ᴇxᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ ᴛᴏ ɪᴍᴘᴏʀᴛ ɪᴛ."
        )

    mystic = await message.reply_text("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")

    async def progress(current, total):
        try:
            await mystic.edit_text(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ... {current * 100 / total:.1f}%")
        except FloodWait as w:
            await asyncio.sleep(w.value)

    file_path = await message.reply_to_message.download(progress=progress)

    try:
        with open(file_path, "r") as backup_file:
            data = json.load(backup_file)
    except (json.JSONDecodeError, IOError):
        return await edit_or_reply(
            mystic, "ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴀ ꜰᴏʀᴍᴀᴛ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴇxᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ"
        )

    if not isinstance(data, dict):
        return await edit_or_reply(
            mystic, "ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴀ ꜰᴏʀᴍᴀᴛ ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴇxᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ"
        )

    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    db = _mongo_async_[DB_NAME]

    try:
        for collection_name, documents in data.items():
            if documents:
                mystic = await edit_or_reply(
                    mystic, f"ɪᴍᴘᴏʀᴛɪɴɢ...\nᴄᴏʟʟᴇᴄᴛɪᴏɴ {collection_name}."
                )
                collection = db[collection_name]

                for document in documents:
                    await collection.replace_one(
                        {"_id": document["_id"]}, document, upsert=True
                    )

        await edit_or_reply(mystic, "ᴅᴀᴛᴀ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ ꜰʀᴏᴍ ʀᴇᴘʟɪᴇᴅ ꜰɪʟᴇ")
    except Exception as e:
        await edit_or_reply(mystic, f"ᴇʀʀᴏʀ ᴅᴜʀɪɴɢ ɪᴍᴘᴏʀᴛ {e}\nʀᴏʟʟɪɴɢ ʙᴀᴄᴋ ᴄʜᴀɴɢᴇꜱ)

    if os.path.exists(file_path):
        os.remove(file_path)
