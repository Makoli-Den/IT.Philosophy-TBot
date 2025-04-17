import re
from telegram import Update
from telegram.ext import ContextTypes
from db.repositories.user_repo import add_user, get_mentions
from db.repositories.chat_repo import add_chat, add_user_to_chat

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
	user = update.effective_user
	chat = update.effective_chat

	await add_user(
		id=user.id,
		username=user.username,
		full_name=user.full_name,
		chat_id=chat.id
	)

	await add_chat(id=chat.id, title=chat.title)

	await add_user_to_chat(user_id=user.id, chat_id=chat.id)

	if not update.message or not update.message.text:
		return

	if re.search(r'@all', update.message.text, re.IGNORECASE):
		mentions = await get_mentions(chat_id=chat.id)

		if mentions:
			await update.message.reply_text(
				"👋 " + " ".join(mentions),
				parse_mode='Markdown'
			)
		else:
			await update.message.reply_text("😕 Не нашёл никого для упоминания.")
