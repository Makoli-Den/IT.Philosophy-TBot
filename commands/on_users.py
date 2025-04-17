import logging
from telegram import Update
from telegram.ext import ContextTypes
from db.models.user import User
from db.repositories.user_repo import get_user
from db.repositories.chat_repo import get_chats

logger = logging.getLogger(__name__)

async def on_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
	logger.debug("Fetching all users from the database.")
	
	try:
		users = await User.all()
		logger.info(f"Successfully fetched {len(users)} users from the database.")
	except Exception as e:
		logger.error(f"Error fetching users: {str(e)}")
		await update.message.reply_text("Произошла ошибка при получении списка пользователей.")
		return
	
	response = "Список пользователей и их чатов:\n\n"

	for user in users:
		try:
			chats = await user.chats.all()
			chat_titles = [chat.title for chat in chats]
			response += f"{user.username} ({user.full_name}): {', '.join(chat_titles) if chat_titles else 'Нет чатов'}\n"
			logger.debug(f"User {user.username} has {len(chats)} chats.")
		except Exception as e:
			logger.error(f"Error fetching chats for user {user.username}: {str(e)}")
			response += f"{user.username} ({user.full_name}): Ошибка при получении чатов.\n"
	
	try:
		await update.message.reply_text(response)
		logger.info("Successfully sent the users list as a reply.")
	except Exception as e:
		logger.error(f"Error sending the users list message: {str(e)}")
		await update.message.reply_text("Произошла ошибка при отправке сообщения.")
