# BeastX - UserBot
# Copyright (C) 2021 msy1717
#
# This file is a part of < https://github.com/msy1717/BeastX/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/msy1717/BeastX-Py/blob/main/LICENSE>.

import asyncio
import os
import time
from random import randint
from urllib.request import urlretrieve

from pytz import timezone
from telethon.errors.rpcerrorlist import ChannelsTooMuchError
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)

from .. import LOGS
from ..configs import Var
from ..functions.helper import download_file, updater


def startup_stuff():
    from .. import mrunal

    x = ["resources/auths", "resources/downloads", "vcbot/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    if CT := mrunal.get("CUSTOM_THUMBNAIL"):
        urlretrieve(CT, "resources/extras/BeastX.jpg")

    if GT := mrunal.get("GDRIVE_TOKEN"):
        with open("resources/auths/auth_token.txt", "w") as t_file:
            t_file.write(GT)

    if (MM := mrunal.get("MEGA_MAIL")) and (MP := mrunal.get("MEGA_PASS")):
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    if TZ := mrunal.get("TIMEZONE"):
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except BaseException:
            LOGS.info(
                "Incorrect Timezone ,\nCheck Available Timezone From Here https://telegra.ph/BeastX-06-18-2\nSo Time is Default UTC"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import mrunal, beastx_bot

    if mrunal.get("BOT_TOKEN"):
        return
    if Var.BOT_TOKEN:
        return mrunal.set("BOT_TOKEN", Var.BOT_TOKEN)
    await beastx_bot.start()
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather, Kindly Wait")
    who = beastx_bot.me
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "BeastX_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await beastx_bot(UnblockRequest(bf))
    await beastx_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await beastx_bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await beastx_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await beastx_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        exit(1)
    await beastx_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await beastx_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await beastx_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await beastx_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            exit(1)
    await beastx_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await beastx_bot.get_messages(bf, limit=1))[0].text
    await beastx_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "Beastx_" + (str(who.id))[6:] + str(ran) + "_bot"
        await beastx_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await beastx_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            mrunal.set("BOT_TOKEN", token)
            await beastx_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await beastx_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await beastx_bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )

            exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        mrunal.set("BOT_TOKEN", token)
        await beastx_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await beastx_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await beastx_bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )

        exit(1)


async def autopilot():
    from .. import asst, mrunal, beastx_bot

    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        mrunal.set("LOG_CHANNEL", str(Var.LOG_CHANNEL))
    if mrunal.get("LOG_CHANNEL"):
        try:
            await beastx_bot.get_entity(int(mrunal.get("LOG_CHANNEL")))
            return
        except BaseException as er:
            LOGS.error(er)
            mrunal.delete("LOG_CHANNEL")
    LOGS.info("Creating a Log Channel for You!")
    try:
        r = await beastx_bot(
            CreateChannelRequest(
                title="BeastX Logs",
                about="My BeasyX Log Group\n\n Join @BeastX_Userbot",
                megagroup=True,
            ),
        )
    except ChannelsTooMuchError:
        LOGS.info(
            "You Are in Too Many Channels & Groups , Leave some And Restart The Bot"
        )
        exit(1)
    except BaseException as er:
        LOGS.info(er)
        LOGS.info(
            "Something Went Wrong , Create A Group and set its id on config var LOG_CHANNEL."
        )
        exit(1)
    chat = r.chats[0]
    chat_id = chat.id
    if not str(chat_id).startswith("-100"):
        mrunal.set("LOG_CHANNEL", "-100" + str(chat_id))
    else:
        mrunal.set("LOG_CHANNEL", str(chat_id))
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    await beastx_bot(EditAdminRequest(chat_id, asst.me.username, rights, "Assistant"))
    photo = await download_file(
        "https://telegra.ph/file/4a1e0ee716f805cf66777.jpg", "channelphoto.jpg"
    )
    ll = await beastx_bot.upload_file(photo)
    await beastx_bot(EditPhotoRequest(chat_id, InputChatUploadedPhoto(ll)))
    os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, mrunal, beastx_bot

    try:
        chat_id = int(mrunal.get("LOG_CHANNEL"))
        if asst.me.photo:
            return
        LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
        UL = f"@{asst.me.username}"
        if (beastx_bot.me.username) is None:
            sir = beastx_bot.me.first_name
        else:
            sir = f"@{beastx_bot.me.username}"
        await beastx_bot.send_message(
            chat_id, "Auto Customisation Started on @botfather"
        )
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", "/start")
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await beastx_bot.send_file(
            "botfather", "resources/extras/assistantpic.jpg"
        )
        await asyncio.sleep(2)
        await beastx_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await beastx_bot.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await beastx_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await beastx_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await beastx_bot.send_message(
            "botfather",
            f"✨ PowerFul BeastX Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @BeastX_UserBot ✨",
        )
        await asyncio.sleep(2)
        await beastx_bot.send_message(
            chat_id, "**Auto Customisation** Done at @BotFather"
        )
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import beastx_bot
    from .utils import load_addons

    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = beastx_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for Plug_channel in plugin_channels.split():
        LOGS.info(f"{'•'*4} {Plug_channel}")
        try:
            if Plug_channel.startswith("@"):
                chat = Plug_channel
            else:
                try:
                    chat = int(Plug_channel)
                except BaseException:
                    return
            async for x in beastx_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                if x.file.name in os.listdir("addons"):
                    LOGS.info(f"Plugin {x.file.name} is Pre Installed")
                    continue
                await asyncio.sleep(0.6)
                file = await beastx_bot.download_media(x.media, "./addons/")
                plugin = x.file.name
                try:
                    load_addons(plugin.replace(".py", ""))
                except Exception as e:
                    LOGS.info(f"BeastX - PLUGIN_CHANNEL - ERROR - {plugin}")
                    LOGS.exception(e)
                    os.remove(file)
        except Exception as e:
            LOGS.exception(e)


# some stuffs
async def ready():
    from .. import asst, mrunal, beastx_bot

    chat_id = int(mrunal.get("LOG_CHANNEL"))
    spam_sent = None
    if not mrunal.get("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """🎇 **Thanks for Deploying BeastX Userbot!**
• Here, are the Some Basic stuff from, where you can Know, about its Usage."""
        PHOTO = "https://telegra.ph/file/4a1e0ee716f805cf66777.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        mrunal.set("INIT_DEPLOY", "Done")
    else:
        MSG = f"**BEAST has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{beastx_bot.me.first_name}](tg://user?id={beastx_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @BeastX_Userbot\n➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        prev_spam = mrunal.get("LAST_UPDATE_LOG_SPAM")
        if prev_spam:
            try:
                await beastx_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info("Error while Deleting Previous Update Message :" + str(E))
        if updater():
            BTTS = Button.inline("Update Available", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await beastx_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await beastx_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    if spam_sent and not spam_sent.media:
        mrunal.set("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    try:
        # To Let Them know About New Updates and Changes
        await beastx_bot(JoinChannelRequest("@BeastX_Userbot"))
        await beastx_bot(JoinChannelRequest("@BeastX_Bots"))

    except ChannelsTooMuchError:
        LOGS.info("Join @BeastX_Userbot to know about new Updates...")
    except Exception as er:
        LOGS.exception(er)
