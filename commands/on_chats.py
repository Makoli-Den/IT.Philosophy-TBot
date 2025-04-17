import logging
from telegram import Update
from telegram.ext import ContextTypes
from db.models.chat import Chat
from db.repositories.chat_repo import get_chats

logger = logging.getLogger(__name__)

async def on_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
	logger.debug("Fetching all chats from the database.")
	
	try:
		chats = await Chat.all()
		logger.info(f"Successfully fetched {len(chats)} chats from the database.")
	except Exception as e:
		logger.error(f"Error fetching chats: {str(e)}")
		await update.message.reply_text("Произошла ошибка при получении списка чатов.")
		return
	
	response = "Список чатов и их пользователей:\n\n"

	for chat in chats:
		try:
			users = await chat.users.all()
			user_names = [user.username for user in users]
			response += f"{chat.title}: {', '.join(user_names) if user_names else 'Нет пользователей'}\n"
			logger.debug(f"Chat {chat.title} has {len(users)} users.")
		except Exception as e:
			logger.error(f"Error fetching users for chat {chat.title}: {str(e)}")
			response += f"{chat.title}: Ошибка при получении пользователей.\n"
	
	try:
		await update.message.reply_text(response)
		logger.info("Successfully sent the chats list as a reply.")
	except Exception as e:
		logger.error(f"Error sending the chats list message: {str(e)}")
		await update.message.reply_text("Произошла ошибка при отправке сообщения.")
