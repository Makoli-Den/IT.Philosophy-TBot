import logging
from config.settings import DB_URL
from tortoise import Tortoise

logger = logging.getLogger(__name__)

async def init_db():
	try:
		logger.info(f"Initializing database connection with URL: {DB_URL}")
		await Tortoise.init(
			db_url=DB_URL,
			modules={
				'models': [
					'db.models.user',
					'db.models.chat'
				]
			}
		)
		logger.info("Database connection established successfully.")
		
		logger.info("Generating database schemas.")
		await Tortoise.generate_schemas()
		logger.info("Schemas generated successfully.")
	except Exception as e:
		logger.error(f"Error during database initialization: {str(e)}", exc_info=True)
