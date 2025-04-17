from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.user_repo import add_user
from db.repositories.chat_repo import add_chat, add_user_to_chat

async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
	chat = update.effective_chat

	await add_chat(id=chat.id, title=chat.title)

	for member in update.message.new_chat_members:
		await add_user(
			id=member.id,
			username=member.username,
			full_name=member.full_name,
			chat_id=chat.id
		)
		
		await add_user_to_chat(chat_id=chat.id, user_id=member.id)
