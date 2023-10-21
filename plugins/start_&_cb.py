
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from helper.database import db
from config import Config, Txt  



# Command to add an admin
@Client.on_message(filters.command("addadmin") & filters.private)
async def add_admin(client, message):
    user_id = message.from_user.id
    await db.add_admin(user_id)
    await message.reply_text("User has been added as an admin.")

# Command to remove an admin
@Client.on_message(filters.command("rmadmin") & filters.private)
async def remove_admin(client, message):
    user_id = message.from_user.id
    await db.remove_admin(user_id)
    await message.reply_text("User has been removed as an admin.")
  
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user is banned
    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        # Send a message indicating that the user is banned
        await message.reply("You are banned by the admin.")
    else:
        # User is not banned, continue with the regular start message
        await db.add_user(client, message)
        button = InlineKeyboardMarkup([[
            InlineKeyboardButton("👨‍💻 Dᴇᴠꜱ 👨‍💻", callback_data='dev')
            ], [
            InlineKeyboardButton('📯 Uᴩᴅᴀᴛᴇꜳ', url='https://t.me/PYRO_BOTZ'),
            InlineKeyboardButton('💁‍♂️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/PYRO_BOTZ_CHAT')
            ], [
            InlineKeyboardButton('🎛️ Aʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('🛠️ Hᴇʟᴩ', callback_data='help')
        ]])
        if Config.START_PIC:
            await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
        else:
            await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

# Add these import statements at the top of your code
from pyrogram.types import Message

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def rban_user(client, message):
    if len(message.command) != 2:
        await message.reply("Usage: /rban [user_id]")
        return

    user_id = int(message.command[1])

    # Ban the user in the database
    await db.ban_user(user_id)

    await message.reply(f"User with ID {user_id} is banned.")

@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def runban_user(client, message):
    if len(message.command) != 2:
        await message.reply("Usage: /runban [user_id]")
        return

    user_id = int(message.command[1])

    # Unban the user in the database
    await db.unban_user(user_id)

    await message.reply(f"User with ID {user_id} is unbanned.")
              
@Client.on_message(filters.private & filters.command("banusers") & filters.user(Config.ADMIN))
async def list_banned_users(client, message):
    # Query the database to get the count of banned users
    banned_count = await db.get_banned_users_count()

    await message.reply(f"Number of users banned by admin: {banned_count}")

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton("👨‍💻 Dᴇᴠꜱ 👨‍💻", callback_data='dev')
                ],[
                InlineKeyboardButton('📯 Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/PYRO_BOTZ'),
                InlineKeyboardButton('💁‍♂️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/PYRO_BOTZ_CHAT')
                ],[
                InlineKeyboardButton('🎛️ Aʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('🛠️ Hᴇʟᴩ', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT")
                ],[
                InlineKeyboardButton("❤️‍🔥 Hᴏᴡ Tᴏ Uꜱᴇ❤️‍🔥", url='https://youtu.be/4ZfvMSDXBVg')
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])            
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT")
                ],[
                InlineKeyboardButton("🖥️ Hᴏᴡ Tᴏ Mᴀᴋᴇ", url="https://youtu.be/GfulqsSnTv4")
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])            
        )
    elif data == "dev":
        await query.message.edit_text(
            text=Txt.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT")
                ],[
                InlineKeyboardButton("🖥️ Hᴏᴡ Tᴏ Mᴀᴋᴇ", url="https://youtu.be/GfulqsSnTv4")
                ],[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data = "start")
            ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()




