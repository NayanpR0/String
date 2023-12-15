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



@Anony.on_message(filters.command("fcast") & filters.user(OWNER_ID))
async def fcast(_, m : Message):
    users = []
    susers = await get_served_users()
    lel = await m.reply_text(text="`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    total_users = len(await get_served_users())
    start_time = time.time()
    for usrs in susers:
        try:
            userid = usrs["user_id"]
            print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            await asyncio.sleep(0.3)
            success +=1
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1
            
        #await asyncio.sleep(2)
        if not success % 20:
            await lel.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {success} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await lel.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nFailed: {failed}")    
    
    
    
    
    #await lel.edit(f"✅Successfull to `{success}` users.\n\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

