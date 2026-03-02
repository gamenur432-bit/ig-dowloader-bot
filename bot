import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
import yt_dlp

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Instagram video link yuboring.")


@dp.message()
async def download_instagram(message: Message):
    url = message.text

    if "instagram.com" not in url:
        await message.answer("Iltimos, to‘g‘ri Instagram link yuboring.")
        return

    await message.answer("⏳ Yuklanmoqda...")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "video.%(ext)s",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = FSInputFile("video.mp4")
        await message.answer_video(video_file)

        os.remove("video.mp4")

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi.")
        print(e)


async def main():
    await dp.start_polling(bot)


if name == "main":
    asyncio.run(main())
