import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"Hello, {user.first_name}! We're currently developing stay tunned!")


application.add_handler(CommandHandler("start", start))

application.run_polling()
