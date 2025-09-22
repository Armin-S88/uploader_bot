import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = "8401810600:AAGHSbX4WiTGVXMYk9hp1LE-mbKAGvXsC-Y"
ADMIN_ID = [5900237205]  # آیدی عددی ادمین‌ها

CHANNELS = [
    "@kos_vpn132",
    "@batman_coin12",
    "@samt_khoda12",
    "@donald_bet132"
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# دیتابیس ساده برای فایل‌ها
try:
    with open("files.json", "r") as f:
        FILES = json.load(f)
except:
    FILES = {}

def save_files():
    with open("files.json", "w") as f:
        json.dump(FILES, f, indent=4)

async def check_subs(user_id):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# ثبت فایل توسط ادمین
@dp.message_handler(commands=["add"])
async def add_file(msg: types.Message):
    if msg.from_user.id not in ADMIN_ID:
        return await msg.reply("❌ فقط ادمین می‌تواند فایل اضافه کند")

    if not msg.reply_to_message or not msg.reply_to_message.document:
        return await msg.reply("⚠️ باید روی یک فایل ریپلای کنید و دستور /add بزنید")

    file_id = msg.reply_to_message.document.file_id
    file_name = msg.reply_to_message.document.file_name
    link_id = str(len(FILES) + 1)

    FILES[link_id] = {"file_id": file_id, "name": file_name}
    save_files()

    start_link = f"https://t.me/{(await bot.get_me()).username}?start=file{link_id}"
    await msg.reply(f"✅ فایل ذخیره شد!\n📎 لینک اختصاصی:\n{start_link}")

# دریافت فایل با لینک استارت
@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    args = msg.get_args()

    if args.startswith("file"):
        file_key = args.replace("file", "")
        if file_key in FILES:
            subscribed = await check_subs(msg.from_user.id)
            if not subscribed:
                channels_list = "\n".join([f"👉 {ch}" for ch in CHANNELS])
                return await msg.reply(f"❌ اول باید در کانال‌ها عضو شوید:\n\n{channels_list}")

            file_data = FILES[file_key]
            await bot.send_document(msg.chat.id, file_data["file_id"], caption=f"📂 {file_data['name']}")
        else:
            await msg.reply("❌ فایل پیدا نشد")
    else:
        await msg.reply("سلام 👋\nبرای دریافت فایل‌ها از لینک اختصاصی استفاده کنید.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
