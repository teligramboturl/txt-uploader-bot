import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import cloudscraper
import m3u8
import random
import yt_dlp
from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import cloudscraper
import m3u8
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Environment variables for API credentials
API_ID = os.environ.get("API_ID", "21705536")
API_HASH = os.environ.get("API_HASH", "c5bb241f6e3ecf33fe68a444e288de2d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

#import os
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# Environment variables for API credentials
API_ID = os.environ.get("API_ID", "21705536")
API_HASH = os.environ.get("API_HASH", "c5bb241f6e3ecf33fe68a444e288de2d")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define the owner's user ID
OWNER_ID = 5957208798  # Replace with the actual owner's user ID

# Lists to store authorized channels, users, and groups
authorized_channels = []
authorized_users = []
authorized_groups = []

# Check if a user is authorized
def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in authorized_users

# Check if a chat (channel/group) is authorized
def is_chat_authorized(chat_id: int) -> bool:
    return chat_id in authorized_channels or chat_id in authorized_groups

# Authorize command to add/remove authorized channels, users, and groups
@bot.on_message(filters.command("authorize"))
async def authorize_command(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    try:
        args = message.text.split(" ", 3)
        if len(args) < 3:
            await message.reply_text("**Usage:** `/authorize <type> <action> <id>`\n\n"
                                   "**Types:** `channel`, `user`, `group`\n"
                                   "**Actions:** `add`, `remove`")
            return

        auth_type = args[1].lower()
        action = args[2].lower()
        target_id = int(args[3])

        if auth_type == "channel":
            if action == "add":
                if target_id not in authorized_channels:
                    authorized_channels.append(target_id)
                    await message.reply_text(f"**✅ Channel ID {target_id} has been authorized.**")
                else:
                    await message.reply_text(f"**⚠️ Channel ID {target_id} is already authorized.**")
            elif action == "remove":
                if target_id in authorized_channels:
                    authorized_channels.remove(target_id)
                    await message.reply_text(f"**➖ Channel ID {target_id} has been removed.**")
                else:
                    await message.reply_text(f"**⚠️ Channel ID {target_id} is not in the authorized list.**")
            else:
                await message.reply_text("**Invalid action. Use `add` or `remove`.**")

        elif auth_type == "user":
            if action == "add":
                if target_id not in authorized_users:
                    authorized_users.append(target_id)
                    await message.reply_text(f"**✅ User ID {target_id} has been authorized.**")
                else:
                    await message.reply_text(f"**⚠️ User ID {target_id} is already authorized.**")
            elif action == "remove":
                if target_id in authorized_users:
                    authorized_users.remove(target_id)
                    await message.reply_text(f"**➖ User ID {target_id} has been removed.**")
                else:
                    await message.reply_text(f"**⚠️ User ID {target_id} is not in the authorized list.**")
            else:
                await message.reply_text("**Invalid action. Use `add` or `remove`.**")

        elif auth_type == "group":
            if action == "add":
                if target_id not in authorized_groups:
                    authorized_groups.append(target_id)
                    await message.reply_text(f"**✅ Group ID {target_id} has been authorized.**")
                else:
                    await message.reply_text(f"**⚠️ Group ID {target_id} is already authorized.**")
            elif action == "remove":
                if target_id in authorized_groups:
                    authorized_groups.remove(target_id)
                    await message.reply_text(f"**➖ Group ID {target_id} has been removed.**")
                else:
                    await message.reply_text(f"**⚠️ Group ID {target_id} is not in the authorized list.**")
            else:
                await message.reply_text("**Invalid action. Use `add` or `remove`.**")

        else:
            await message.reply_text("**Invalid type. Use `channel`, `user`, or `group`.**")

    except Exception as e:
        await message.reply_text(f"**Error:** {str(e)}")

# List authorized channels, users, and groups
@bot.on_message(filters.command("list_authorized"))
async def list_authorized_command(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID:
        await message.reply_text("**🚫 You are not authorized to use this command.**")
        return

    response = (
        f"**Authorized Channels:** {', '.join(map(str, authorized_channels)) or 'None'}\n"
        f"**Authorized Users:** {', '.join(map(str, authorized_users)) or 'None'}\n"
        f"**Authorized Groups:** {', '.join(map(str, authorized_groups)) or 'None'}"
    )
    await message.reply_text(response)

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/Engineers_Babu"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/Engineers_Babu"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/Engineersbabuupdates"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://i.postimg.cc/t428ZHY7/02.webp",
    "https://i.postimg.cc/6QkC6yLK/03.webp",
    "https://i.postimg.cc/fbdNhHf8/04.webp",
    "https://i.postimg.cc/yxMGnKwB/05.webp",
    "https://i.postimg.cc/50ddnwvD/06.webp",
    "https://i.postimg.cc/wT7zxT6f/07.webp",
    "https://i.postimg.cc/pVk0GfM4/08.webp",
    "https://i.postimg.cc/1tBLrbKY/09.webp",
]
random_image_url = random.choice(image_urls)

# Define the caption
caption = (
    "**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫👋!**\n\n"
    "➠ **𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️**\n"
    "➠ **Can Extract Videos & PDFs From Your Text File and Upload to Telegram!**\n"
    "➠ **For Guide Use Command /guide 📖**\n"
    "➠ **Use /Upload Command to Download From TXT File** 📄\n"
    "➠ **𝐌𝐚𝐝𝐞 𝐁𝐲:** @Engineers_Babu"
)

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if the user is authorized
    if not is_authorized(user_id):
        await message.reply_text("**🚫 You are not authorized to use this bot.**")
        return

    # Check if the chat (channel/group) is authorized
    if message.chat.type in ["channel", "group", "supergroup"] and not is_chat_authorized(chat_id):
        await message.reply_text("**🚫 This chat is not authorized to use this bot.**")
        return

    await bot.send_photo(chat_id=message.chat.id, photo=random_image_url, caption=caption, reply_markup=keyboard)

# Stop command handler
@bot.on_message(filters.command("stop"))
async def stop_command(bot: Client, message: Message):
    if not is_authorized(message.from_user.id):
        await message.reply_text("**🚫 You are not authorized to use this bot.**")
        return

    await message.reply_text("**Bot stopped.** 🚦")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Upload command handler
@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐀 𝐓𝐱𝐭 𝐅𝐢𝐥𝐞 𝐒𝐞𝐧𝐝 𝐇𝐞𝐫𝐞 📄')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)
    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        
        # Extract the title from the file name
        file_name = os.path.basename(x)  # Get the file name from the path
        raw_text0 = os.path.splitext(file_name)[0]  # Remove the file extension to get the title
        
        os.remove(x)
            # print(len(links)
    except:
           await m.reply_text("**∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.**")
           os.remove(x)
           return
        
    await editable.edit(f"**∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n**𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐢𝐚𝐥 𝐢𝐬** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**∝ 🎬 𝐄𝐧𝐭𝐞𝐫 𝐑𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 \n➤ 𝟏𝟒𝟒ᴘ - 𝐬ᴇɴᴅ 144 \n ➤ 𝟐𝟒𝟎ᴘ - 𝐬ᴇɴᴅ 240 \n ➤ 𝟑𝟔𝟎ᴘ - 𝐬ᴇɴᴅ 360 \n ➤ 𝟒𝟖𝟎ᴘ - 𝐬ᴇɴᴅ 480 \n ➤ 𝟕𝟐𝟎ᴘ - 𝐬ᴇɴᴅ 720 \n ➤ 𝟏𝟎𝟖𝟎ᴘ - 𝐬ᴇɴᴅ 1080 **")
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

    await editable.edit("𝐍𝐨𝐰 𝐄𝐧𝐭𝐞𝐫 𝐘𝐨𝐮𝐫 𝐍𝐚𝐦𝐞 𝐭𝐨 𝐚𝐝𝐝 𝐜𝐚𝐩𝐭𝐢𝐨𝐧 𝐨𝐧 𝐲𝐨𝐮𝐫 𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐟𝐢𝐥𝐞")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MPH = highlighter 
    else:
        MPH = raw_text3

    #await editable.edit("**𝐄𝐧𝐭𝐞𝐫 𝐘𝐨𝐮𝐫 𝐏𝐖 𝐓𝐨𝐤𝐞𝐧 𝐅𝐨𝐫 𝐌𝐏𝐃 𝐔𝐑𝐋 𝐨𝐫 𝐬𝐞𝐧𝐝 '𝐮𝐧𝐤𝐧𝐨𝐰𝐧' 𝐟𝐨𝐫 𝐮𝐬𝐞 𝐝𝐞𝐟𝐚𝐮𝐥𝐭**")
    #input4: Message = await bot.listen(editable.chat.id)
    #raw_text4 = input4.text
    #await input4.delete(True)
    #if raw_text4 == 'unknown':
        #MR = token
    #else:
        #MR = raw_text4
   
    await editable.edit("🌄 𝐍𝐨𝐰 𝐬𝐞𝐧𝐝 𝐭𝐡𝐞 𝐓𝐡𝐮𝐦𝐛 𝐔𝐑𝐋 \n 𝐄𝐠. » https://i.postimg.cc/d1JW4kb6/01.jpg \n 𝐎𝐫 𝐢𝐟 𝐝𝐨𝐧'𝐭 𝐰𝐚𝐧𝐭 𝐭𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥 𝐬𝐞𝐧𝐝 = 𝐧𝐨")
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

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","") #.replace("youtube.com/embed/", "youtube.com/watch?v=") # .replace("mpd","m3u8")
            url = "https://" + V

            
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

             #Classplus
            elif 'videos.classplusapp' in url:
             headers = {
                    'host': 'api.classplusapp.com',
                    'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9',    
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
             res = requests.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", params=params, headers=headers).json()
             print(res)
                
            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}0', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']
            elif 'tencdn.classplusapp' in url or 'media-cdn-alisg.classplusapp.com' in url or 'videos.classplusapp' in url or ('media-cdn.classplusapp' in url):
                headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                params = (('url', f'{url}'),)
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                url = response.json()['url']
            
            elif 'videos.classplusapp' in url or "tencdn.classplusapp" in url or "webvideos.classplusapp.com" in url or "media-cdn-alisg.classplusapp.com" in url or "videos.classplusapp" in url or "videos.classplusapp.com" in url or "media-cdn-a.classplusapp" in url or "media-cdn.classplusapp" in url:
             url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0'}).json()['url']
                
            #cpvod    
            if 'testbook' in url:
                id =  url.split("/")[-2]
                url =  "https://extractapi.vercel.app/classplus?link=https://cpvod.testbook.com/" + id + "/playlist.m3u8"

            elif 'cpvod.testbook' in url:
                id =  url.split("/")[-2]
                url =  "https://extractapi.vercel.app/classplus?link=https://cpvod.testbook.com/" + id + "/playlist.m3u8"
                            
            #Utkarshapp
            elif '/utkarshapp.mpd' in url:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
             id =  url.split("/")[-2]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
             url =  "https://apps-s3-prod.utkarshapp.com/" + id + "/utkarshapp.com"

            elif "apps-s3-jw-prod.utkarshapp.com" in url:
                if 'enc_plain_mp4' in url:
                    url = url.replace(url.split("/")[-1], res+'.mp4')
                    
                elif 'Key-Pair-Id' in url:
                    url = None
                    
                elif '.m3u8' in url:
                    q = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).split("/")[0]
                    x = url.split("/")[5]
                    x = url.replace(x, "")
                    url = ((m3u8.loads(requests.get(url).text)).data['playlists'][1]['uri']).replace(q+"/", x)

            #physicswallah
            
            elif '/master.mpd' in url:
             vid_id =  url.split("/")[-2]
                url =  f"https://madxapi-d0cbf6ac738c.herokuapp.com/{vid_id}/master.m3u8?token={raw_text4}"

            if "/master.mpd" in url :
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/","https://d1d34p8vz63oiq.cloudfront.net/")
                    print(url)
                else: 
                    url = url    

                print("mpd check")
                key = await helper.get_drm_keys(url)
                print(key)
                await m.reply_text(f"got keys form api : \n`{key}`")

            elif '/master.mpd' in url:
                 id =  url.split("/")[-2]
                 url =  "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"
                
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'
          
            if "/master.mpd" in url:
                cmd= f" yt-dlp -k --allow-unplayable-formats -f bestvideo.{raw_text2} --fixup never {url} "
                print("counted")

            #Carrerwill
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            if 'psitoffers.store' in url:
                 vid_id = url.split("vid=")[1].split("&")[0]
                 print(f"vid_id = {vid_id}")
                 url =  f"https://madxapi-d0cbf6ac738c.herokuapp.com/{vid_id}/master.m3u8?token={raw_text4}"
            
        
            if raw_text0 in "vikramjeet" :
                y= url.replace("/", "%2F")
#                rout = f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2Flivehttporigin%2F{y[56:-14]}%2Fmaster.m3u8"
                rout =f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2F{y[39:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"
                # print (rout)
                # print(url)
            elif raw_text0 in "sure60":
                y1= url.replace("/", "%2F")
#                rout = f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2Flivehttporigin%2F{y[49:-14]}%2Fmaster.m3u8"
                rout =f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2F{y1[32:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"            
            elif raw_text0 in "theoptimistclasses":
                y= url.replace("/", "%2F")
                rout=f"https://live.theoptimistclasses.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.theoptimistclasses.com%2F{y[44:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')              
                cook = "cookie.txt"

            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            if 'acecwply' in url:
            cmd = f'yt-dlp -o "{name}" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif 'youtu' in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}"'
            elif 'player.vimeo' in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}"'
            elif 'm3u8' or 'livestream' in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == '0' or 'unknown' in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}"'
            elif '.pdf' or 'download' in url:
                cmd = 'pdf'
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}"'
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            if "embed" in url:
            ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'


            try:  
                
                cc = f'**🎞️ 𝐕𝐈𝐃_𝐈𝐃: {str(count).zfill(3)}.\n\n📄 𝐓𝐢𝐭𝐥𝐞: {name1} .mkv\n📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 » {raw_text0}\n📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲 » {MPH}**\n\n**{centered_text}**'
                cc1 = f'**📁 𝐏𝐃𝐅_𝐈𝐃: {str(count).zfill(3)}.\n\n📄 𝐓𝐢𝐭𝐥𝐞: {name1} .pdf\n📚 𝐁𝐚𝐭𝐜𝐡 𝐍𝐚𝐦𝐞 » {raw_text0}\n📥 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐝 𝐁𝐲 » {MPH}**\n\n{centered_text}**'
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
                    copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                    count += 1
                    os.remove(f'{name}.pdf')
                except FloodWait as e:
                    await m.reply_text(str(e))
                    time.sleep(e.x)
                    continue

            elif ".pdf" in url:
                try:
                    await asyncio.sleep(4)
                    # Replace spaces with %20 in the URL
                    url = url.replace(" ", "%20")

                    # Create a cloudscraper session
                    scraper = cloudscraper.create_scraper()

                    # Send a GET request to download the PDF
                    response = scraper.get(url)

                    # Check if the response status is OK
                    if response.status_code == 200:
                        # Write the PDF content to a file
                        with open(f'{name}.pdf', 'wb') as file:
                            file.write(response.content)

                        # Send the PDF document
                        await asyncio.sleep(4)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                        count += 1

                        # Remove the PDF file after sending
                        os.remove(f'{name}.pdf')
                    else:
                        await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                except FloodWait as e:
                    await m.reply_text(str(e))
                    await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                    return  # Exit the function to avoid continuation

                except Exception as e:
                    await m.reply_text(f"An error occurred: {str(e)}")
                    await asyncio.sleep(4)  # You can replace this with more specific
                    continue
                else:
                    Show = f"**❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊... »**\n\n**📝 𝐍𝐚𝐦𝐞 »** `{name}\n**❄ 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}`\n**🔗𝐔𝐑𝐋 »** `[Hidden]`\n\n{centered_text}**"
                    prog = await m.reply_text(Show)
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("**✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞**")


bot.run()
