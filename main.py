import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = "7514993033:AAFtqumIZ6qkVaEtv2mSgXrwLt9AzxZPHbs"

CHANNEL_USERNAME = "@persian_gulf_league2017"

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    print(f"/start از کاربر: {user_id}")
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo='AgACAgQAAxkBAAM2aGQCHZSJ2Sc-85EqWuYCmhpo2k4AAubJMRsWxCBToGxp3GIHeVMBAAMCAAN5AAM2BA'
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("✅ ربات روشنه و آماده کاره!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
