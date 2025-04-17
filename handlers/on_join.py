import logging
from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.user_repo import add_user
from db.repositories.chat_repo import add_chat, add_user_to_chat

logger = logging.getLogger(__name__)

async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		chat = update.effective_chat
		logger.info(f"New members joining chat: {chat.id} - {chat.title}")

		await add_chat(id=chat.id, title=chat.title)
		logger.info(f"Chat {chat.id} added to the database.")

		for member in update.message.new_chat_members:
			logger.info(f"Adding user {member.id} to chat {chat.id}")

			await add_user(
				id=member.id,
				username=member.username,
				full_name=member.full_name
			)
			logger.info(f"User {member.id} added to the database.")

			await add_user_to_chat(chat_id=chat.id, user_id=member.id)
			logger.info(f"User {member.id} added to chat {chat.id}")
	except Exception as e:
		logger.error(f"Error in on_join handler: {str(e)}", exc_info=True)
