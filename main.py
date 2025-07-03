import nest_asyncio
import asyncio
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
)
from telegram.error import BadRequest

nest_asyncio.apply()

BOT_TOKEN = "7514993033:AAEcp__u4U0avuku2dvFhvb69kCgU7uw6LI"
OWNER_ID = 5599905266
CHANNEL_ID = -1002737874150
BOT_USERNAME = "persian_gulf_league2017_bot"

REQUIRED_CHANNELS = [
    "@persian_gulf_league2017",
    "@filmtrolll",
    "@Twittrol",
    "@Sportrolll"
]

stored_files = set()

def extract_message_id(link: str):
    match = re.search(r"/(\d+)$", link)
    return int(match.group(1)) if match else None

async def is_user_member(bot, user_id, channel_username):
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ("member", "creator", "administrator")
    except BadRequest:
        return False

async def check_memberships_all(bot, user_id):
    for channel in REQUIRED_CHANNELS:
        if not await is_user_member(bot, user_id, channel):
            return False
    return True

async def ask_join_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = "\n".join([f"🔗 {ch}" for ch in REQUIRED_CHANNELS])
    text = f"""برای دریافت فایل، باید عضو این کانال‌ها بشی:

{links}

بعد از عضویت، روی دکمه زیر بزن 👇"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")]
    ])
    await update.message.reply_text(text, reply_markup=keyboard)

async def check_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    bot = context.bot

    is_member = await check_memberships_all(bot, user_id)
    if is_member:
        await query.edit_message_text("✅ عضویت شما تایید شد. حالا می‌تونید فایل دریافت کنید.")
    else:
        await query.edit_message_text("❌ هنوز عضو همه‌ی کانال‌ها نشدی. لطفاً عضو شو و دوباره امتحان کن.")
        await ask_join_channels(update, context)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if user_id != OWNER_ID:
        is_member = await check_memberships_all(context.bot, user_id)
        if not is_member:
            await ask_join_channels(update, context)
            return

    if user_id == OWNER_ID and not args:
        await update.message.reply_text("لینک پیام کانال رو بفرست تا لینک فایل ساخته بشه.")
        return

    if args:
        msg_id_str = args[0]
        if not msg_id_str.isdigit():
            await update.message.reply_text("کد نامعتبره.")
            return
        msg_id = int(msg_id_str)
        if msg_id not in stored_files:
            await update.message.reply_text("فایل پیدا نشد یا حذف شده.")
            return
        try:
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=msg_id
            )
        except Exception as e:
            await update.message.reply_text(f"خطا در ارسال فایل: {e}")
        return

    await update.message.reply_text("برای دریافت فایل، لینک مخصوص فایل رو وارد کن.")

async def handle_owner_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        return

    if update.message.text:
        msg_id = extract_message_id(update.message.text)
        if msg_id:
            stored_files.add(msg_id)
            link = f"https://t.me/{BOT_USERNAME}?start={msg_id}"
            await update.message.reply_text(f"✅ لینک فایل ساخته شد:\n{link}")
            return

    await update.message.reply_text("لینک پیام کانال رو بفرست.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_owner_message))

    print("✅ ربات روشنه و آماده کاره!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
