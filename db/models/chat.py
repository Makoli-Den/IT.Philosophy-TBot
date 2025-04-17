import logging
from tortoise import fields, models
from tortoise.exceptions import DoesNotExist
from tortoise.fields.relational import ManyToManyRelation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from db.models.user import User

logger = logging.getLogger(__name__)

class Chat(models.Model):
	id = fields.IntField(pk=True)
	title = fields.CharField(max_length=256, null=True)

	users: ManyToManyRelation["User"] = fields.ManyToManyField(
		"models.User",
		related_name="chats"
	)

	class Meta:
		table = "chat"

	def __str__(self):
		return self.title

	@classmethod
	async def create_chat(cls, id: int, title: str):
		try:
			logger.debug(f"Trying to create chat with id: {id} and title: {title}")
			chat = await cls.create(id=id, title=title)
			logger.info(f"Chat with id: {id} created successfully.")
			return chat
		except Exception as e:
			logger.error(f"Error while creating chat with id: {id}: {str(e)}")
			raise

	@classmethod
	async def get_chat_by_id(cls, id: int):
		try:
			logger.debug(f"Trying to fetch chat with id: {id}")
			chat = await cls.get(id=id)
			logger.info(f"Chat with id: {id} fetched successfully.")
			return chat
		except DoesNotExist:
			logger.warning(f"Chat with id: {id} does not exist.")
			return None
		except Exception as e:
			logger.error(f"Error while fetching chat with id: {id}: {str(e)}")
			raise
