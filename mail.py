
import imaplib
import email
from email.header import Header, decode_header, make_header
import base64
from bs4 import BeautifulSoup
import re

import asyncio
import logging
from aiogram.exceptions import TelegramBadRequest

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from utils.settings import Config 
from aiogram.types import CallbackQuery, Message

async def start(message: types.Message):
    await message.answer(message.text)

async def login():
    config_data = Config("config.txt")
    mail_pass = config_data.mail_pass
    username = config_data.username
    imap_server = config_data.imap_server
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    return imap

def decoder(subject: str) -> str:
    first_pos = subject.find("=?") 
    second_pos = subject.rfind("?=") 
    if (first_pos != -1) and (second_pos != -1):
        h = str(make_header(decode_header(subject)))
        return h
    return subject

async def select_new_last_message() -> str:
    config_data = Config("config.txt")
    imap = await login()
    imap.select(config_data.mail_folder)
    retcode, messages = (imap.uid('search', "UNSEEN", "ALL"))
    if retcode != "OK" or not messages[0].split():
        return "None"
    theme_id =  (messages[0].split()[-1])
    res, msg = imap.uid('fetch', theme_id, '(RFC822)')  #Для метода uid
    msg = email.message_from_bytes(msg[0][1])

    letter_date = email.utils.parsedate_tz(msg["Date"]) # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
    letter_theme = msg["Subject"] # e-mail отправителя
    
    date_msg = f"{letter_date[0]}-{letter_date[1]}-{letter_date[2]} {letter_date[3]}:{letter_date[4]}:{letter_date[5]}"
    letter_theme = decoder(letter_theme)
    info_msg = f"<b>Date:</b> {date_msg}\n<b>Theme:</b> {letter_theme}"
    imap.close()
    imap.logout()
    return (info_msg)
# 

async def check_school_mail(bot: Bot):
    config_data = Config("config.txt")
    while True:
        try:
            message = "No messages yet"
            message = await select_new_last_message()
            if (message != "None"):
                await bot.send_message(config_data.id, message)
            await asyncio.sleep(3)
        except TimeoutError:
            await asyncio.sleep(5)


async def main():
    dp = Dispatcher()
    dp.message.register(start, (Command(commands=["start"])))
    logging.basicConfig(level=logging.INFO)
    config_data = Config("config.txt")
    bot = Bot(token=config_data.token, parse_mode="html")
    await asyncio.gather(dp.start_polling(bot), check_school_mail(bot))

if __name__ == "__main__":
    asyncio.run(main())
