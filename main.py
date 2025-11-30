from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message
from pyrogram import Client, filters
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
import time
import asyncio
from pyrogram.types import User, Message
from config import api_id, api_hash, bot_token, auth_users, sudo_users
import sys
import re
import os

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)

@bot.on_message(filters.command(["stop"]))
async def cancel_command(bot: Client, m: Message):
    user_id = m.from_user.id if m.from_user is not None else None
    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply(f"**You Are Not Subscribed To This Bot\nContact - @Mahagoraxyz**", quote=True)
        return
    await m.reply_text("**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    
    user_id = m.from_user.id if m.from_user is not None else None

    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply(f"**You Are Not Subscribed To This Bot\nContact - @Mahagoraxyz**", quote=True)
        return
        
    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)
            
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send `de` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'de':
        CR = credit
    else:
        CR = raw_text3

    await editable.edit("**Enter Your PW/Classplus Woking Token\n\nOtherwise Send 'no'**")
    input4: Message = await bot.listen(editable.chat.id)
    working_token = input4.text
    await input4.delete(True)

    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send 'no'")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):
            # ✅ FIX 1: Check if link is valid
            if len(links[i]) < 2 or not links[i][1]:
                await m.reply_text(f"❌ Skipping invalid link: {links[i]}")
                count += 1
                continue
                
            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url_match = re.search(r"(https://.*?playlist.m3u8.*?)\"", text)
                        if url_match:
                            url = url_match.group(1)
                        else:
                            await m.reply_text("❌ Visionias URL not found")
                            continue

            elif 'classplusapp' in url or "testbook.com" in url or "classplusapp.com/drm" in url or "media-cdn.classplusapp.com/drm" in url:
                # ✅ FIX 2: Skip if token is invalid
                if working_token.lower() == "no" or not working_token or "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9" in working_token:
                    await m.reply_text("🚫 Classplus token invalid, trying direct download...")
                    # Direct download try karo
                    try:
                        name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                        name = f'{str(count).zfill(3)}) {name1[:60]}'
                        cc1 = f'** {str(count).zfill(3)}.** {name1}\n**Batch Name :**{b_name}\n\n**Downloaded by : {CR}**'
                        
                        prog = await m.reply_text(f"**Downloading Direct:-**\n\n**Name :-** `{name}`\n**link:**`{url}`")
                        res_file = await helper.download_video(url, name, raw_text2)
                        filename = res_file
                        await prog.delete(True)
                        await helper.send_vid(bot, m, cc1, filename, thumb, name)
                        count += 1
                        continue
                    except Exception as e:
                        await m.reply_text(f"❌ Direct download failed: {e}")
                        count += 1
                        continue
                    
                headers = {
                    'host': 'api.classplusapp.com',
                    'x-access-token': f'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTYzNTU1MzA0LCJvcmdJZCI6MTAwNTg1OSwidHlwZSI6MSwibW9iaWxlIjoiOTE3NTY4Mjg3NjM5IiwibmFtZSI6Ik1hbmlzaCIsImVtYWlsIjoibTc1NjgyODc2MzlAZ21haWwuY29tIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJjb3VudHJ5SVNPIjoiOTEiLCJ0aW1lem9uZSI6IkdNVCs1OjMwIiwiaXNEaXkiOnRydWUsIm9yZ0NvZGUiOiJidWlqamsiLCJpc0RpeVN1YmFkbWluIjowLCJmaW5nZXJwcmludElkIjoiMjcyNWE0MDgxYWQ3NDA4MWIxZDJkZjc4NGRhNjJiYTMiLCJpYXQiOjE3NjQ0OTYxNzEsImV4cCI6MTc2NTEwMDk3MX0.oyJxarFpGY3WxUBDU_7cNmU_XZOmfcQOg9vMyvWkofMFQJ_BOndv5Q1gXWcEom_r',    
                    'accept-language': 'EN',
                    'api-version': '18',
                    'app-version': '1.4.73.2',
                    'build-number': '35',
                    'connection': 'Keep-Alive',
                    'content-type': 'application/json',
                    'device-details': 'Xiaomi_Redmi 7_SDK-32',
                    'device-id': 'c28d3cb16bbdac01',
                    'region': 'IN',
                    'user-agent': 'Mobile-Android',
                    'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c',
                    'accept-encoding': 'gzip'
                }
                
                url = url.replace('https://tencdn.classplusapp.com/', 'https://media-cdn.classplusapp.com/tencent/')

                params = {
                    "url": f"{url}"
                }

                try:
                    response = requests.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", params=params, headers=headers)
                    
                    if response.status_code == 200:
                        res = response.json()
                        if "url" in res:
                            if "testbook.com" in url or "classplusapp.com/drm" in url or "media-cdn.classplusapp.com/drm" in url:
                                url = res['drmUrls']['manifestUrl']
                            else:
                                url = res["url"]
                        else:
                            await m.reply_text(f"❌ CP API Error: {res}")
                            continue
                    else:
                        await m.reply_text(f"❌ CP API Failed: Status {response.status_code}")
                        continue
                except Exception as e:
                    await m.reply_text(f"❌ CP API Failed: {e}")
                    continue

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                if working_token.lower() == "no" or not working_token:
                    await m.reply_text("❌ PW token required but not provided")
                    continue
                url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={url}?token={working_token}"
                
            else:
                url = url
                
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'
            
            try:                               
                cc = f'** {str(count).zfill(3)}.** {name1}\n**Batch Name :** {b_name}\n\n**Downloaded by : {CR}**'
                cc1 = f'** {str(count).zfill(3)}.** {name1}\n**Batch Name :**{b_name}\n\n**Downloaded by : {CR}**'
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                elif ".pdf" in url:
                    try:
                        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id,document=f'{name}.pdf', caption=cc1)
                        count += 1
                        os.remove(f'{name}.pdf')
                        continue
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    prog = await m.reply_text(f"**Downloading:-**\n\n** Video Name :-** `{name}\nQuality - {raw_text2}`\n**link:**`{url}`**")
                    res_file = await helper.download_video(url, name, raw_text2)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name)
                    count += 1

            except Exception as e:
                await m.reply_text(f"**This #Failed File is not Counted**\n**Name** =>> `{name}`\n**Link** =>> `{url}`\n\n ** fail reason »** {e}")
                count += 1
                continue

    except Exception as e:
        await m.reply_text(f"Main Error: {e}")
    await m.reply_text("🔰Done Boss🔰")


bot.run()
