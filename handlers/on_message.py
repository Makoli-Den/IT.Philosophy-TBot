import re
import logging
from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.user_repo import add_user, get_mentions
from db.repositories.chat_repo import add_chat, add_user_to_chat

logger = logging.getLogger(__name__)

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	try:
		user = update.effective_user
		chat = update.effective_chat

		logger.debug(f"Received message from user {user.id} in chat {chat.id}")

		await add_user(
			id=user.id,
			username=user.username,
			full_name=user.full_name,
		)
		logger.info(f"Added user {user.id} to database.")

		await add_chat(id=chat.id, title=chat.title)
		logger.info(f"Added chat {chat.id} to database.")

		await add_user_to_chat(user_id=user.id, chat_id=chat.id)
		logger.info(f"Added user {user.id} to chat {chat.id}.")

		if not update.message or not update.message.text:
			logger.debug("Received message without text.")
			return

		logger.debug(f"Message text: {update.message.text}")

		if re.search(r'@all', update.message.text, re.IGNORECASE):
			mentions = await get_mentions(chat_id=chat.id)
			logger.debug(f"Mentions found: {mentions}")

			if mentions:
				await update.message.reply_text(
					"👋 " + " ".join(mentions),
					parse_mode='Markdown'
				)
				logger.info(f"Replied with mentions to user {user.id} in chat {chat.id}")
			else:
				await update.message.reply_text("😕 Не нашёл никого для упоминания.")
				logger.info(f"No mentions found for chat {chat.id}")
	except Exception as e:
		logger.error(f"Error in on_message handler: {str(e)}", exc_info=True)
