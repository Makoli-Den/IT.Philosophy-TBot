from config.settings import DB_URL
from tortoise import Tortoise

async def init_db():
	await Tortoise.init(
		db_url=DB_URL,
		modules={
			'models': [
				'db.models.user',
				'db.models.chat'
			]
		}
	)
	await Tortoise.generate_schemas()
