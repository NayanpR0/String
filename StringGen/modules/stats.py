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
    await message.reply_text(f"» ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛs ᴏғ {Anony.name} :\n\n {users} ᴜsᴇʀs")

async def delete_user(user_id):
        await usersdb.delete_many({'user_id': int(user_id)})

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ, ꜱɪɴᴄᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} - ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - ᴘᴇᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ")
        return False, "Error"
    except Exception as e:
        return False, "Error"


@Anony.on_message(filters.command("fcast") & filters.user(OWNER_ID))
async def fcast(_, m : Message):
    users = []
    susers = await get_served_users()
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    total_users = len(await get_served_users())
    start_time = time.time()
    for user in susers:
        users.append(int(user["user_id"]))
    for i in users:
        pti, sh = await m.reply_to_message.forward(i)
        if pti:
            success += 1
        elif pti == False:
            if errors.UserIsBlocked:
                blocked+=1
            elif errors.InputUserDeactivated:
                deleted += 1
                remove_user(userid)
            elif errors.PeerIdInvalid:
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await lel.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await lel.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed}")    
    
    
    
    
    #await lel.edit(f"✅Successfull to `{success}` users.\n\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")



@Anony.on_message(filters.command("broadcast") & filters.user(OWNER_ID) & filters.reply)
async def verupikkals(_, message: Message):
    users = usersdb
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = len(await get_served_users())
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    #for user in users:
    for user in usersdb.find():
        pti, sh = await broadcast_messages(int(user['user_id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed")    
