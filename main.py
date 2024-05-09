import asyncio
import json
import logging
import os
import re
import subprocess
import sys
import time
from logging.handlers import RotatingFileHandler
from subprocess import getstatusoutput

import requests
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyromod import listen

import online.helpers.vid as helper
from online.Config import *
from online.helpers.button import keyboard
from online.helpers.sudoers import *
from online.helpers.text import *

# ==========Logging==========#
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("Assist.txt", maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging = logging.getLogger()

# =========== Client ===========#
bot = Client(
    "bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
)

print(listen.__file__)


paid_text = """
» Hello i am online class bot which help you to **Download** videos and pdf from T**XT FILE**.
• **How to Access this bot**

Step 1: Click Below on Developer.
Step 2: Go to Telegram Username
Step 3: Send your Telegram ID From @missrose_bot
"""


# ============== Start Commands ==========#
@bot.on_message(filters.command(["start"]))
async def account_lstarn(bot: Client, m: Message):
    if not one(m.from_user.id):
        return await m.reply_photo(
            photo="https://graph.org/file/89210bbddd0c095db6a6b.jpg",
            caption=paid_text,
            reply_markup=keyboard,
        )
    await m.reply_photo(
          photo="https://graph.org/file/89210bbddd0c095db6a6b.jpg",
          caption=start_text,
          reply_markup=keyboard,
)


# ========== Global Concel Command ============
cancel = False


@bot.on_message(filters.command(["cancel"]))
async def cancel(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nThis Command is only For Owner",
            reply_markup=keyboard,
        )
    editable = await m.reply_text(
        "Canceling All process Plz wait\n🚦🚦 Last Process Stopped 🚦🚦"
    )
    global cancel
    cancel = False
    await editable.edit("cancelled all")
    return


# ============== Power Commands =================
@bot.on_message(filters.command("restart"))
async def restart_handler(_, m):
    if not two(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nYou Don't Have Right To Access This Contact Owner",
        )
    await m.reply_text("➭ 𝗕𝗼𝘁 𝗥𝗲𝘀𝘁𝗮𝗿𝘁𝗲𝗱 🥰", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


# ============ Download Commands ==============#
@bot.on_message(filters.command(["txt1"]))
async def download_pw(bot: Client, m: Message):
    global cancel
    m.from_user.id if m.from_user is not None else None
    if not one(m.from_user.id):
        return await m.reply_text(
            "✨ Hello Sir,\n\nContact Me Click Below",
            reply_markup=keyboard,
        )
    else:
        editable = await m.reply_text(pyro_text, disable_web_page_preview=True)
    input = await bot.listen(editable.chat.id)
    x = await input.download()
    links = []
    try:
        with open(x, "r") as f:
            content = f.read()
            new_content = content.split("\n")
            for i in new_content:
                links.append(re.split(":(?=http)", i))
        os.remove(x)
    except Exception as e:
        await m.reply_text(f"**Error** : {e}")
        os.remove(x)
        return
    await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    initial_number = await bot.listen(editable.chat.id)

    try:
        arg = int(initial_number.text)
    except:
        arg = 0

    await m.reply_text(
        f"Total links: **{len(links)}**\n\nSend Me Final Number\n\nBy Default Final is {len(links)}"
    )
    final_number = await bot.listen(editable.chat.id)

    try:
        arg1 = int(final_number.text)
    except:
        arg1 = len(links)
    await m.reply_text("**Enter batch name**")
    input0 = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text(
        "**For Thumb Url**\n\n• Custom url : Use @vtelegraphbot and send me links\n• If Your file Contain Url : `yes`\n• Send no if you don't want : `no`"
    )
    input6 = await bot.listen(editable.chat.id)
    lol_thumb = input6.text

    if arg == "0":
        count = 1
    else:
        count = int(arg)
    cancel = True
    for i in range(arg, arg1):
        try:
            while cancel == False:
                return await m.reply_text("Cancelled Process")
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )
            try:
                if lol_thumb == "yes":
                    old_thumb = links[i][2]
                    getstatusoutput(f"wget '{old_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                elif lol_thumb.startswith("http://") or lol_thumb.startswith(
                    "https://"
                ):
                    old_thumb = lol_thumb
                    getstatusoutput(f"wget '{lol_thumb}' -O 'thumb.jpg'")
                    thumb = "thumb.jpg"
                else:
                    thumb = "no"
                    old_thumb = "No Thumbnail"
            except Exception as e:
                return await m.reply_text(e)
            Total_Links = arg1 - int(arg)
            Show_old = f"**Total Links** : {Total_Links}\n\n**Name :-** `{name1}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
            prog_old = await m.reply_text(Show_old)
            if raw_text2 == "144":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "256x144" in out:
                    ytf = f"{out['256x144']}"
                elif "320x180" in out:
                    ytf = out["320x180"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "320x180" in out:
                    ytf = out["320x180"]
                elif "426x240" in out:
                    ytf = out["426x240"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "426x240" in out:
                    ytf = out["426x240"]
                elif "426x234" in out:
                    ytf = out["426x234"]
                elif "480x270" in out:
                    ytf = out["480x270"]
                elif "480x272" in out:
                    ytf = out["480x272"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                logging.info(out)
                if "640x360" in out:
                    ytf = out["640x360"]
                elif "638x360" in out:
                    ytf = out["638x360"]
                elif "636x360" in out:
                    ytf = out["636x360"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "638x358" in out:
                    ytf = out["638x358"]
                elif "852x316" in out:
                    ytf = out["852x316"]
                elif "850x480" in out:
                    ytf = out["850x480"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["852x470"]
                elif "1280x720" in out:
                    ytf = out["1280x720"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "854x480" in out:
                    ytf = out["854x480"]
                elif "852x480" in out:
                    ytf = out["852x480"]
                elif "854x470" in out:
                    ytf = out["854x470"]
                elif "768x432" in out:
                    ytf = out["768x432"]
                elif "848x480" in out:
                    ytf = out["848x480"]
                elif "850x480" in out:
                    ytf = ["850x480"]
                elif "960x540" in out:
                    ytf = out["960x540"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]
            elif raw_text2 == "720":
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if "1280x720" in out:
                    ytf = out["1280x720"]
                elif "1280x704" in out:
                    ytf = out["1280x704"]
                elif "1280x474" in out:
                    ytf = out["1280x474"]
                elif "1920x712" in out:
                    ytf = out["1920x712"]
                elif "1920x1056" in out:
                    ytf = out["1920x1056"]
                elif "854x480" in out:
                    ytf = out["854x480"]
                elif "640x360" in out:
                    ytf = out["640x360"]
                elif "unknown" in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == "144":
                    ytf = "http-240p"
                elif raw_text2 == "240":
                    ytf = "http-240p"
                elif raw_text2 == "360":
                    ytf = "http-360p"
                elif raw_text2 == "480":
                    ytf = "http-540p"
                elif raw_text2 == "720":
                    ytf = "http-720p"
                else:
                    ytf = "http-360p"
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]

            try:
                if "unknown" in out:
                    pass
                else:
                    list(out.keys())[list(out.values()).index(ytf)]

                name = f"{name1}"
            except Exception as e:
                return await m.reply(f"Error in ytf : {e}")
            await prog_old.delete(True)
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "vision" or "youtu" in url:
                cmd = f'yt-dlp "{url}" -o "{name}"'
            elif "youtu" in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif url.startswith("https://apni-kaksha.vercel.app"):
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == "0" or "unknown" in out:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ".pdf" or "download" in str(url):
                cmd = "pdf"
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'

            try:
                Show = f"**Downloading:-**\n\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-** `{url}`\n**Thumb :-** `{old_thumb}`"
                prog = await m.reply_text(Show)
                cc = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                cc1 = f"**➭ Name » {name1}** \n**➭ Batch » {raw_text0}**"
                if cmd == "pdf" or ".pdf" in str(url) or ".pdf" in name:
                    print("PDF")
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        await m.reply_document(
                            ka,
                            caption=f"{cc1}",
                        )
                        count += 1
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    filename = await helper.download_video(url, cmd, name)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`"
                )
                continue
        except Exception as e:
            return await m.reply_text(f"Overall Error : {e}")
    await m.reply_text("Done")


@bot.on_message(filters.command(["adda_pdf"]))
async def addaspsdin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**bhag bhosadi ke**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am adda pdf Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** :Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    await m.reply_text("**Enter Token**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text

    if raw_text == "0":
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace(":", "")
                .replace("*", "")
                .replace(".", "")
                .replace("'", "")
                .replace('"', "")
                .strip()
            )
            name = f"{str(count).zfill(3)} {name1}"
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`"
            prog = await m.reply_text(Show)
            cc = f"{str(count).zfill(3)}. {name1}.pdf\n"
            try:
                getstatusoutput(
                    f'curl --http2 -X GET -H "Host:store.adda247.com" -H "user-agent:Mozilla/5.0 (Linux; Android 11; moto g(40) fusion Build/RRI31.Q1-42-51-8; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.98 Mobile Safari/537.36" -H "accept:*/*" -H "x-requested-with:com.adda247.app" -H "sec-fetch-site:same-origin" -H "sec-fetch-mode:cors" -H "sec-fetch-dest:empty" -H "referer:https://store.adda247.com/build/pdf.worker.js" -H "accept-encoding:gzip, deflate" -H "accept-language:en-US,en;q=0.9" -H "cookie:cp_token={raw_text5}" "{url}" --output "{name}.pdf"'
                )
                await m.reply_document(f"{name}.pdf", caption=cc)
                count += 1
                await prog.delete(True)
                os.remove(f"{name}.pdf")
                time.sleep(2)
            except Exception as e:
                await m.reply_text(
                    f"{e}\nDownload Failed\n\nName : {name}\n\nLink : {url}"
                )
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")


@bot.on_message(filters.command(["pro_olive"]))
async def proolsgin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("bhag bhosadi ke", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am Oliveboard Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** : Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.readlines()
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total Videos found in this Course are **{len(content)}**\n\nSend From where you want to download initial is **1**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    raw_text5 = input.document.file_name.replace(".txt", "")
    await input.delete(True)
    editable4 = await m.reply_text("**Send thumbnail url**\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    try:
        for count, i in enumerate(
            range(int(raw_text) - 1, len(content)), start=int(raw_text)
        ):
            name1, link = content[i].split(":", 1)
            url = requests.get(
                f"https://api.telegramadmin.ga/olive/link={link}"
            ).json()["m3u8"]
            cook = None

            name = f"{str(count).zfill(3)}) {name1}"
            Show = (
                f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n`"
            )
            prog = await m.reply_text(Show)
            cc = f"**Name »** {name1}.mp4\n**Batch »** {raw_text5}\n**Index »** {str(count).zfill(3)}\n\n**Download BY** :- Group Admin"
            if "olive" or "youtu" in url:
                cmd = f'yt-dlp "{url}" -o "{name}"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "bestvideo+bestaudio" --no-keep-video "{url}" -o "{name}"'
            else:
                cmd = f'yt-dlp -o "{name}" --add-header "cookie: {cook}" "{url}"'
            try:
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                count += 1

                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n"
                )
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


@bot.on_message(filters.command(["pro_jw"]))
async def projwin(bot: Client, m: Message):
    user = m.from_user.id if m.from_user is not None else None
    if user is not None and user not in sudo_users:
        await m.reply("**TUM BHOSADI WALE NIKKAL LO**", quote=True)
        return
    else:
        editable = await m.reply_text(
            "Hello Bruh **I am jw Downloader Bot**. I can download videos from **text** file one by one.**\n\nLanguage** : Python**\nFramework** :Pyrogram\n\nSend **TXT** File {Name : Link}",
            reply_markup=keyboard,
        )
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    editable = await m.reply_text(
        f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**"
    )
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable = await m.reply_text("**Enter Title**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    input2.text

    editable4 = await m.reply_text(
        "Now send the **Thumb url**\nEg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**"
    )
    input6 = message = await bot.listen(editable.chat.id)
    input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == "0":
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):
            url = links[i][1]
            name1 = (
                links[i][0]
                .replace("\t", "")
                .replace(":", "")
                .replace("/", "")
                .replace("+", "")
                .replace("#", "")
                .replace("|", "")
                .replace("@", "")
                .replace("*", "")
                .replace(".", "")
                .strip()
            )

            if "jwplayer" in url:
                headers = {
                    "Host": "api.classplusapp.com",
                    "x-access-token": "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0",
                    "user-agent": "Mobile-Android",
                    "app-version": "1.4.37.1",
                    "api-version": "18",
                    "device-id": "5d0d17ac8b3c9f51",
                    "device-details": "2848b866799971ca_2848b8667a33216c_SDK-30",
                    "accept-encoding": "gzip",
                }

                params = (("url", f"{url}"),)

                response = requests.get(
                    "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
                    headers=headers,
                    params=params,
                )
                # print(response.json())
                a = response.json()["url"]
                # print(a)

                headers1 = {
                    "User-Agent": "ExoPlayerDemo/1.4.37.1 (Linux;Android 11) ExoPlayerLib/2.14.1",
                    "Accept-Encoding": "gzip",
                    "Host": "cdn.jwplayer.com",
                    "Connection": "Keep-Alive",
                }

                response1 = requests.get(f"{a}", headers=headers1)

                url1 = (response1.text).split("\n")[2]

            #                 url1 = b
            else:
                url1 = url

            name = f"{str(count).zfill(3)}) {name1}"
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url1}`"
            prog = await m.reply_text(Show)
            cc = f"**Title »** {name1}.mkv\n**Caption »** {raw_text0}\n**Index »** {str(count).zfill(3)}\n\n**Download BY** :- Group Admin"
            if "pdf" in url:
                cmd = f'yt-dlp -o "{name}.pdf" "{url1}"'
            else:
                cmd = (
                    f'yt-dlp -o "{name}.mp4" --no-keep-video --remux-video mkv "{url1}"'
                )
            try:
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)

                if os.path.isfile(f"{name}.mkv"):
                    filename = f"{name}.mkv"
                elif os.path.isfile(f"{name}.mp4"):
                    filename = f"{name}.mp4"
                elif os.path.isfile(f"{name}.pdf"):
                    filename = f"{name}.pdf"

                #                 filename = f"{name}.mkv"
                subprocess.run(
                    f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"',
                    shell=True,
                )
                await prog.delete(True)
                reply = await m.reply_text(f"Uploading - ```{name}```")
                try:
                    if thumb == "no":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    await m.reply_text(str(e))

                dur = int(helper.duration(filename))

                start_time = time.time()
                if "pdf" in url1:
                    await m.reply_document(filename, caption=cc)
                else:
                    await m.reply_video(
                        filename,
                        supports_streaming=True,
                        height=720,
                        width=1280,
                        caption=cc,
                        duration=dur,
                        thumb=thumbnail,
                        progress=progress_bar,
                        progress_args=(reply, start_time),
                    )
                count += 1
                os.remove(filename)

                os.remove(f"{filename}.jpg")
                await reply.delete(True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed ❌**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}` & `{url1}`"
                )
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")

bot.run()
