import os
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from bot.utils import Storage

storage = Storage('storage')

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

application = Application.builder().token(TOKEN).build()


async def request_approval(user: telegram.User):
    approval_users = storage.get_users(permission=5)
    for approval_user in approval_users:
        print(approval_user['id'])
        await application.bot.send_message(chat_id=str(approval_user['id']), text=f"User {user.full_name} ({user.id}) is seeking approval.")


def unique_user(user: telegram.User):
    if not storage.get_user(user.id):
        storage.create_user(user.id, user.full_name)
        return True
    else:
        return False


def approved_user(user: telegram.User):
    if storage.get_user(user.id).get('permission') != '0':
        return True
    else:
        return False


async def on_start(update: Update, context: CallbackContext):
    user = update.effective_user

    if unique_user(user):
        await update.message.reply_text("We are creating account for you. Wait for approval.")
        print('REQUEST')
        await request_approval(user)

    await update.message.reply_text(f"Hello, {user.first_name}! We're currently developing, stay tuned!")


async def on_message(update: Update, context: CallbackContext):
    user = update.effective_user

    if unique_user(user):
        await update.message.reply_text("We are creating account for you. Wait for approval.")
        print('REQUEST')
        await request_approval(user)
    else:
        if approved_user(user):
            await update.message.reply_text(f"Nice to see you back, {user.first_name}!")
        else:
            await update.message.reply_text("Your account is not yet approved.")


application.add_handler(CommandHandler("start", on_start))
application.add_handler(MessageHandler(None, on_message))
application.run_polling()
