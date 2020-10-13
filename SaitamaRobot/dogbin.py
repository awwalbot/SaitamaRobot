import logging
import os
from nicegrill import utils
from requests import post, get
from telethon.tl.types import MessageEntityUrl

URL = "https://del.dog/"

class Dogbin:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    async def pastexxx(message):
        msg = utils.get_arg(message)
        repmsg = await message.get_reply_message()
        if repmsg:
            await message.edit("<i>Pasting..</i>")
            if repmsg.document and repmsg.document.mime_type == "text/plain":
                doc = await repmsg.download_media()
                with open(doc, "r") as file:
                    context = file.read().encode()
                os.remove(doc)
            elif repmsg.message:
                context = repmsg.message.encode()
            else:
                await message.edit("<i>Input or reply to some text to paste</i>")
                return
            paste = post(f"{URL}documents", data=context).json()
        elif msg:
            await message.edit("<i>Pasting..</i>")
            paste = post(f"{URL}documents", data=msg.encode()).json()
        else:
            await message.edit("<i>Input or reply to some text to paste</i>")
            return
        if paste["key"]:
            await message.edit(
                "<i>Your text pasted successfully.\n"
                f"Here's the link:</i> {URL + paste['key']}")
        else:
            await message.edit("<i>Something went wrong</i>")

    async def getpastexxx(message):
        if message.is_reply:
            reply = await message.get_reply_message()
            link = False
            for entity in reply.entities:
                if isinstance(entity, MessageEntityUrl):
                    link = reply.message[entity.offset: entity.offset + entity.length]
            if not link:
                await message.edit("<i>You didn't specify a dogbin URL</i>")
                return
            await message.edit("<i>Fetching..</i>")
        elif utils.get_arg(message):
            link = utils.get_arg(message)
            await message.edit("<i>Fetching..</i>")
        else:
            await message.edit("<i>You didn't specify a dogbin URL</i>")
            return
        if not link.startswith(f"{URL}"):
            await message.edit("<i>Not a valid URL</i>")
            return
        if "raw" in link.split("/"):
            getpaste = get(link)
        else:
            link = link.split("/")
            link.insert(-1, "raw")
            print(link)
            link = "/".join(link)
            getpaste = get(link)
        await message.edit(getpaste.text)