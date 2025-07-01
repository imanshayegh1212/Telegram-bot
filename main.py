import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

BOT_TOKEN = "7514993033:AAFtqumIZ6qkVaEtv2mSgXrwLt9AzxZPHbs"
CHANNEL_USERNAME = "@persian_gulf_league2017"

async def is_user_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print(f"/start از کاربر: {user_id}")

    if await is_user_member(user_id, context):
        await update.message.reply_photo(photo="AgACAgQAAxkBAAM2aGQCHZSJ2Sc-85EqWuYCmhpo2k4AAubJMRsWxCBToGxp3GIHeVMBAAMCAAN5AAM2BA")
        await update.message.reply_text("✅ خوش اومدی!")
    else:
        await update.message.reply_text(
            f"❗️ برای استفاده از این ربات، باید عضو کانال بشی:\n\n🔗 {CHANNEL_USERNAME}\n\nوقتی عضو شدی، دستور /start رو دوباره بفرست."
        )

# این تابع برای دریافت عکس از کاربر و چاپ File ID عکس‌هاست (برای تست یا توسعه)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.photo[-1].file_id
    print("📸 File ID:", file_id)
    await update.message.reply_text(f"File ID:\n{file_id}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("✅ ربات روشنه و آماده کاره!")
    await app.run_polling()

asyncio.run(main())