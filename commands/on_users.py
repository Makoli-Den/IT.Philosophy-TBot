from telegram import Update
from telegram.ext import ContextTypes
from db.models.user import User
from db.repositories.user_repo import get_user
from db.repositories.chat_repo import get_chats

async def on_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
	users = await User.all()

	response = "Список пользователей и их чатов:\n\n"

	for user in users:
		# Получаем все чаты пользователя
		chats = await user.chats.all()
		chat_titles = [chat.title for chat in chats]
		
		response += f"{user.username} ({user.full_name}): {', '.join(chat_titles) if chat_titles else 'Нет чатов'}\n"
	
	await update.message.reply_text(response)
