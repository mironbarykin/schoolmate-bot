import os
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
from bot.utils import database as db

database = db.Database().manager()

TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

application = Application.builder().token(TOKEN).build()


async def request_approval(user: telegram.User):
    for approver in database.filter_users(access=5):

        message = await application.bot.send_message(chat_id=str(approver['id']), text=f"User {user.full_name} ({user.id}) is seeking approval.")
        database.request_approval(message.message_id, approver['id'], user.id)


def unique_user(user: telegram.User):
    if not database.get_user(user.id):
        database.new_user(user.id, user.full_name)
        return True
    else:
        return False


def approved_user(user: telegram.User):
    if database.get_user(user.id).get('access') != 0:
        return True
    else:
        return False


async def on_start(update: Update, context: CallbackContext):
    user = update.effective_user

    if unique_user(user):
        await update.message.reply_text("We are creating account for you. Wait for approval.")
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
    
    if database.get_user(user.id).get('access') > 5:
        if update.message.reply_to_message:
            original_message = update.message.reply_to_message
            approval = database.get_approval(original_message.message_id)
            if approval:
                if '👍' in update.message.text:
                    await update.message.reply_text(f'Approved.')
                    database.response_approval(True, original_message.message_id)
                    await application.bot.send_message(approval.get('requester_id'), f"Your account is approved by {database.get_user(approval.get('approver_id')).get('name')}")
                elif '👎' in update.message.text:
                    await update.message.reply_text(f'Denied.')
                    database.response_approval(False, original_message.message_id)
                    await application.bot.send_message(approval.get('requester_id'), f"Your account is not confirmed. Denied.")
                else:
                    pass

application.add_handler(CommandHandler("start", on_start))
application.add_handler(MessageHandler(filters.BaseFilter(), on_message))
application.run_polling()
