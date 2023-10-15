from pyrogram import Client, filters 
from helper.database import db

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    user = message.from_user
    user_id = user.id

    # Check if the user is banned
    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        # Send a message indicating that the user is banned
        await message.reply_text("You are banned by the admin.")
    else:
        if len(message.command) == 1:
            return await message.reply_text("**__Give the caption__\n\nExample: `/set_caption {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`**")
        caption = message.text.split(" ", 1)[1]
        await db.set_caption(user_id, caption=caption)
        await message.reply_text("__**✅ Caption Saved**__")

# Repeat the same structure for other command handlers

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        caption = await db.get_caption(user_id)
        if not caption:
            return await message.reply_text("__**😔 You don't have any caption**__")
        await db.set_caption(user_id, caption=None)
        await message.reply_text("__**❌️ Caption Deleted**__")

# Repeat the same structure for other command handlers

@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        caption = await db.get_caption(user_id)
        if caption:
            await message.reply_text(f"**Your Caption:-**\n\n`{caption}`")
        else:
            await message.reply_text("__**😔 You don't have any caption**__")

# Repeat the same structure for other command handlers

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        thumb = await db.get_thumbnail(user_id)
        if thumb:
            await client.send_photo(chat_id=message.chat.id, photo=thumb)
        else:
            await message.reply_text("😔 __**You don't have any thumbnail**__")

# Repeat the same structure for other command handlers

@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        await db.set_thumbnail(user_id, file_id=None)
        await message.reply_text("❌️ __**Thumbnail Deleted**__")

# Repeat the same structure for other command handlers

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    user = message.from_user
    user_id = user.id

    is_banned = await db.is_user_banned(user_id)

    if is_banned:
        await message.reply_text("You are banned by the admin.")
    else:
        mkn = await message.reply_text("Please Wait ...")
        await db.set_thumbnail(user_id, file_id=message.photo.file_id)
        await mkn.edit("✅️ __**Thumbnail Saved**__")
