import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Instagram link yuboring.")

@dp.message()
async def download_instagram(message: Message):
    url = message.text

    if "instagram.com" not in url:
        await message.answer("To‘g‘ri link yuboring.")
        return

    await message.answer("Yuklanmoqda...")

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': 'video.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await message.answer_video(types.FSInputFile("video.mp4"))
        os.remove("video.mp4")

    except:
        await message.answer("Xatolik yuz berdi.")

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
