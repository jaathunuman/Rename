import os 
import speedtest 
import wget 
from pyrogram import Client, filters  
from pyrogram.types import Message  
from config import ADMINS 
 
@Client.on_message(filters.command("speedtest") & filters.user(Config.ADMIN) & filters.reply)
async def run_speedtest(client: Bot, message: Message): 
    m = await message.reply_text("⚡️ Running Server Speedtest") 
    try: 
        test = speedtest.Speedtest() 
        test.get_best_server() 
         
        m = await m.edit("⚡️ Running Download Speedtest..") 
        download_speed = test.download() / 1024 / 1024  # Convert to Mbps 
         
        m = await m.edit("⚡️ Running Upload Speedtest...") 
        upload_speed = test.upload() / 1024 / 1024  # Convert to Mbps 
         
        test.results.share() 
        result = test.results.dict() 
    except Exception as e: 
        await m.edit(str(e))  # Convert exception to string before editing 
        return 
     
    m = await m.edit("🔄 Sharing Speedtest Results") 
    path = wget.download(result["share"]) 
     
    output = f"""💡 <b>SpeedTest Results</b> 
<u><b>Client:</b></u> 
<b>ISP:</b> {result['client']['isp']} 
<b>Country:</b> {result['client']['country']} 
<u><b>Server:</b></u> 
<b>Name:</b> {result['server']['name']} 
<b>Country:</b> {result['server']['country']}, {result['server']['cc']} 
<b>Sponsor:</b> {result['server']['sponsor']} 
⚡️ <b>Ping:</b> {result['ping']} 
🚀 <b>Download Speed:</b> {download_speed:.2f} Mbps 
🚀 <b>Upload Speed:</b> {upload_speed:.2f} Mbps""" 
     
    msg = await client.send_photo( 
        chat_id=message.chat.id, photo=path, caption=output, parse_mode="html" 
    ) 
    os.remove(path) 
    await m.delete()
