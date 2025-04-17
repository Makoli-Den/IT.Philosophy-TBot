from telegram import Update
from telegram.ext import ContextTypes
from db.models.chat import Chat
from db.repositories.chat_repo import get_chats

async def on_chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
	chats = await Chat.all()
	response = "Список чатов и их пользователей:\n\n"

	for chat in chats:
		users = await chat.users.all()
		user_names = [user.username for user in users]

		response += f"{chat.title}: {', '.join(user_names) if user_names else 'Нет пользователей'}\n"

	await update.message.reply_text(response)
