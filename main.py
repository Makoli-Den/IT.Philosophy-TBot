import asyncio
import nest_asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.on_chats import on_chats
from commands.on_users import on_users
from handlers.on_message import on_message
from handlers.on_join import on_join
from handlers.on_left import on_left
from config.settings import BOT_TOKEN
from db.init import init_db
from utils.logger import Logger

logger = Logger.get_logger()

async def main():
	logger.info('Initializing DB.')

	try:
		await init_db()
		logger.info('DB Initialized.')
	except Exception as e:
		logger.error(f"Error initializing DB: {e}")
		return

	logger.info('Starting Bot.')
	try:
		app = ApplicationBuilder().token(BOT_TOKEN).build()
		logger.info('Bot started.')
	except Exception as e:
		logger.error(f"Error starting bot: {e}")
		return

	try:
		app.add_handler(CommandHandler("users", on_users))
		app.add_handler(CommandHandler("chats", on_chats))

		app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
		app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_join))
		app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, on_left))

		logger.debug('Handlers successfully added.')
	except Exception as e:
		logger.error(f"Error adding handlers: {e}")
		return

	logger.info('Polling started.')
	try:
		await app.run_polling(poll_interval=1)
	except Exception as e:
		logger.error(f"Error during polling: {e}")
		return

if __name__ == '__main__':
	nest_asyncio.apply()

	try:
		asyncio.run(main())
	except Exception as e:
		logger.critical(f"Critical error: {e}")
