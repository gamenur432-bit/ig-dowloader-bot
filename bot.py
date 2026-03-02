import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
import yt_dlp

# Bot tokenini muhit o'zgaruvchisidan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    # Agar Replit-da bo'lsangiz, Secrets bo'limiga BOT_TOKEN qo'shganingizga ishonch hosil qiling
    raise ValueError("BOT_TOKEN topilmadi! Iltimos, Secrets bo'limini tekshiring.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Assalomu alaykum! Instagram video linkini yuboring, men uni yuklab beraman. 📥")

@dp.message()
async def download_instagram(message: Message):
    url = message.text

    if "instagram.com" not in url:
        return # Shunchaki javob bermaslik yoki ogohlantirish

    status_msg = await message.answer("⏳ Yuklanmoqda, iltimos kuting...")

    # Fayl nomi har bir foydalanuvchi uchun alohida bo'lishi kerak (xatolik oldini olish uchun)
    file_path = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": file_path,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        # yt-dlp blocking funksiya bo'lgani uchun uni alohida thread-da ishlatish tavsiya etiladi
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))

        if os.path.exists(file_path):
            video_file = FSInputFile(file_path)
            await message.answer_video(video_file, caption="Tayyor! ✅")
            await status_msg.delete()
            
            # Faylni yuborgandan so'ng o'chirish
            os.remove(file_path)
        else:
            await message.answer("❌ Videoni yuklashda muammo bo'ldi.")

    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi. Link noto'g'ri yoki video yopiq profilda bo'lishi mumkin.")
        print(f"Xato: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if name == "main":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")
