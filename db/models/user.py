import logging
from tortoise import fields, models
from tortoise.exceptions import DoesNotExist
from tortoise.fields.relational import ManyToManyRelation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from db.models.chat import Chat

logger = logging.getLogger(__name__)

class User(models.Model):
	id = fields.IntField(pk=True)
	username = fields.CharField(max_length=64, null=True)
	full_name = fields.CharField(max_length=128, null=True)

	chats: ManyToManyRelation["Chat"]

	class Meta:
		table = "user"

	def __str__(self):
		return self.username or self.full_name

	@classmethod
	async def create_user(cls, id: int, username: str, full_name: str):
		try:
			logger.debug(f"Trying to create user with id: {id}, username: {username}, full_name: {full_name}")
			user = await cls.create(id=id, username=username, full_name=full_name)
			logger.info(f"User with id: {id} created successfully.")
			return user
		except Exception as e:
			logger.error(f"Error while creating user with id: {id}: {str(e)}")
			raise

	@classmethod
	async def get_user_by_id(cls, id: int):
		try:
			logger.debug(f"Trying to fetch user with id: {id}")
			user = await cls.get(id=id)
			logger.info(f"User with id: {id} fetched successfully.")
			return user
		except DoesNotExist:
			logger.warning(f"User with id: {id} does not exist.")
			return None
		except Exception as e:
			logger.error(f"Error while fetching user with id: {id}: {str(e)}")
			raise
