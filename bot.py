import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
import yt_dlp

# Xatoliklarni kuzatish uchun logging
logging.basicConfig(level=logging.INFO)

# Tokenni muhit o'zgaruvchisidan olish (GitHub Secrets yoki .env uchun)
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Iltimos, muhit o'zgaruvchilarini tekshiring.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Assalomu alaykum! Menga Instagram video linkini yuboring.")

@dp.message()
async def download_instagram(message: Message):
    url = message.text

    if "instagram.com" not in url:
        return # Faqat instagram linklariga javob beradi

    status_msg = await message.answer("⏳ Yuklanmoqda...")
    
    # Har bir foydalanuvchi uchun alohida fayl nomi (bir vaqtda ishlatilganda xato bermasligi uchun)
    file_path = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": file_path,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        # yt-dlp ni bloklamaydigan rejimda ishga tushirish
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))

        if os.path.exists(file_path):
            video_file = FSInputFile(file_path)
            await message.answer_video(video_file, caption="Yuklab olindi! ✅")
            await status_msg.delete()
            
            # Faylni yuborgandan so'ng o'chirish
            os.remove(file_path)
        else:
            await message.answer("❌ Videoni yuklab bo'lmadi.")

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi. Link noto'g'ri yoki video yopiq profilda bo'lishi mumkin.")
        print(f"Error log: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)

async def main():
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

# ASOSIY TUZATISH: name va "main" ikkita chiziq bilan yoziladi
if name == "main":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
