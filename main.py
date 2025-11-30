from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os
import time
from config import api_id, api_hash, bot_token, auth_users, sudo_users

bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@bot.on_message(filters.command(["start"]))
async def start_cmd(bot: Client, m: Message):
    if m.from_user.id not in auth_users and m.from_user.id not in sudo_users:
        await m.reply("❌ You are not authorized!")
        return
    
    await m.reply("📁 Send me TXT file with links")

@bot.on_message(filters.document)
async def handle_txt_file(bot: Client, m: Message):
    if m.from_user.id not in auth_users and m.from_user.id not in sudo_users:
        return

    if not m.document.file_name.endswith('.txt'):
        await m.reply("❌ Please send TXT file only")
        return

    # Download file
    file = await m.download()
    
    with open(file, 'r') as f:
        links = f.readlines()
    
    os.remove(file)
    
    await m.reply(f"📊 Found {len(links)} links. Starting download...")
    
    success = 0
    failed = 0
    
    for i, link in enumerate(links, 1):
        link = link.strip()
        if not link:
            continue
            
        try:
            if '.pdf' in link:
                # PDF download
                cmd = f'yt-dlp -o "file_{i}.pdf" "{link}"'
                os.system(cmd)
                await bot.send_document(m.chat.id, f"file_{i}.pdf", caption=f"PDF {i}")
                os.remove(f"file_{i}.pdf")
                success += 1
                
            else:
                # Video download (direct links only)
                cmd = f'yt-dlp -o "file_{i}.mp4" "{link}"'
                os.system(cmd)
                await bot.send_video(m.chat.id, f"file_{i}.mp4", caption=f"Video {i}")
                os.remove(f"file_{i}.mp4")
                success += 1
                
        except Exception as e:
            await m.reply(f"❌ Failed {i}: {e}")
            failed += 1
            
        time.sleep(2)  # Avoid flooding
    
    await m.reply(f"✅ Done!\nSuccess: {success}\nFailed: {failed}")

bot.run()
