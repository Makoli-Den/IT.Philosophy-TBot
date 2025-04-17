from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.chat_repo import remove_user_from_chat

async def on_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
	chat = update.effective_chat
	user = update.message.left_chat_member

	await remove_user_from_chat(user_id=user.id, chat_id=chat.id)
