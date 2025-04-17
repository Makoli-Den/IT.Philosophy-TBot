import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.on_chats import on_chats
from commands.on_users import on_users
from handlers.on_message import on_message
from handlers.on_join import on_join
from handlers.on_left import on_left
from config.settings import BOT_TOKEN
from db.init import init_db

async def main():
	print('Initializing DB.')
	await init_db()
	print('DB Initialized.')

	print('Starting Bot.')
	app = ApplicationBuilder().token(BOT_TOKEN).build()
	print('Bot started.')

	app.add_handler(CommandHandler("users", on_users))
	app.add_handler(CommandHandler("chats", on_chats))

	app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
	app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_join))
	app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_left))

	print('Polling.')
	await app.run_polling(poll_interval=1)

if __name__ == '__main__':
	nest_asyncio.apply()
	asyncio.run(main())
