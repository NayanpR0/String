from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatInviteLink
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from StringGen import Anony
from StringGen.utils import add_served_user, keyboard
from config import SESSION_STRING, API_ID, API_HASH
#REQUEST_CHANNEL_ID = int("REQUEST_CHANNEL_ID", "-1001545900924")
REQUEST_CHANNEL_ID = "-1001859813868"

userbot = Client(
    "approver222",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=str(config.SESSION_STRING)
)

userbot.start()

@Anony.on_message(filters.command("start") & filters.private & filters.incoming)
async def f_start(_, message: Message):
    await add_served_user(message.from_user.id)
    try:
        await Anony.get_chat_member(-1001859813868, message.from_user.id)
    except UserNotParticipant:
        generator = userbot.get_chat_join_requests(-1001859813868)
        users_ids = [ChatJoiner.user.id async for ChatJoiner in generator]
        if message.from_user.id not in users_ids:
            buttons = [[
                InlineKeyboardButton("ʀᴇqᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/+C2MKCc8BrIJhNzNl")
            ],[
                InlineKeyboardButton("Try Again", "chk")
            ]]
            return await message.reply("ʜᴇʏ {message.from_user.first_name},\n\nᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ ᴄʟɪᴄᴋ ʀᴇQᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʜᴇɴ ᴛʀʏ ᴀɢᴀɪɴ", reply_markup=InlineKeyboardMarkup(buttons), quote=True)

    
@Anony.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await Anony.get_chat_member(-1001859813868, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            await cb.message.edit("**ʜᴇʏ {cb.from_user.first_name},\n\n๏ ᴛʜɪs ɪs {Anony.mention},\nAɴ ᴏᴘᴇɴ sᴏᴜʀᴄᴇ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ, ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴩʏʀᴏɢʀᴀᴍ.**", reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name +"  started Your Bot!")
    except UserNotParticipant:
        await cb.answer("❌ ꜱᴇɴᴅ ʀᴇqᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴏᴜʀ ʙᴏᴛ ✅ ")


