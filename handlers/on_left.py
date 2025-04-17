import logging
from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.chat_repo import remove_user_from_chat

logger = logging.getLogger(__name__)

async def on_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		chat = update.effective_chat
		user = update.message.left_chat_member

		logger.info(f"User {user.id} left chat {chat.id}")

		await remove_user_from_chat(user_id=user.id, chat_id=chat.id)
		logger.info(f"Removed user {user.id} from chat {chat.id}")
	except Exception as e:
		logger.error(f"Error in on_left handler: {str(e)}", exc_info=True)
