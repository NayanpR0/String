from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
import datetime
import time
import asyncio

from config import OWNER_ID
from StringGen import Anony
from StringGen.utils import get_served_users, usersdb

@Anony.on_message(filters.command(["stats", "users"]) & filters.user(OWNER_ID))
async def get_stats(_, message: Message):
    users = len(await get_served_users())
    await message.reply_text(f"» ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {Anony.mention} :\n\n {users} ᴜsᴇʀs")



@Anony.on_message(filters.command(["broadcast", "stat"]) & filters.user(OWNER_ID))
async def broadcast(_, m: Message):
    if m.text == "/stat":
        total_users = await usersdb.count_documents({})
        return await m.reply(f"ᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}")
    b_msg = m.reply_to_message
    sts = await m.reply_text("ʙʀᴏᴀᴅᴄᴀꜱᴛɪɴɢ...")
    users = usersdb.find({})
    total_users = await usersdb.count_documents({})
    done = 0
    failed = 0
    blocked = 0
    success = 0
    start_time = time.time()
    async for user in users:
        user_id = int(user['user_id'])
        try:
            await b_msg.copy(chat_id=user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await b_msg.copy(chat_id=user_id)
            success += 1
        except InputUserDeactivated:
            await usersdb.delete_many({'id': user_id})
            failed += 1
        except UserIsBlocked:
            blocked += 1
        except PeerIdInvalid:
            await usersdb.delete_many({'id': user_id})
            failed += 1
        except Exception as e:
            failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss:\n\nᴛᴏᴛᴀʟ ᴜsᴇʀs {total_users}\nᴄᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\nsᴜᴄᴄᴇss: {success}\nʙʟᴏᴄᴋᴇᴅ: {blocked}\nғᴀɪʟᴇᴅ: {failed}\n\nʙᴏᴛ - {Anony.mention}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await m.reply_text(f"ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ:\nᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time_taken} sᴇᴄᴏɴᴅs.\n\nᴛᴏᴛᴀʟ ᴜsᴇʀs {total_users}\nᴄᴏᴍᴘʟᴇᴛᴇᴅ: {done} / {total_users}\nsᴜᴄᴄᴇss: {success}\nʙʟᴏᴄᴋᴇᴅ: {blocked}\nғᴀɪʟᴇᴅ: {failed}\n\nʙᴏᴛ - {Anony.mention}", quote=True)
