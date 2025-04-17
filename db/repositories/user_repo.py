import logging
from db.models.user import User
from db.models.chat import Chat
from tortoise.exceptions import DoesNotExist
from utils.user_utils import format_mention

logger = logging.getLogger(__name__)

async def add_user(id: int, username: str, full_name: str):
	try:
		logger.debug(f"Trying to get user with id: {id}")
		user = await User.get(id=id)
		logger.info(f"User with id: {id} already exists.")
	except DoesNotExist:
		logger.info(f"User with id: {id} does not exist, creating new one.")
		user = await User.create(id=id, username=username, full_name=full_name)
		logger.info(f"User with id: {id} created successfully.")
	
	return user

async def remove_user(id: int, chat_id: int):
	try:
		logger.debug(f"Trying to remove user with id: {id} from chat with id: {chat_id}")
		user = await User.get(id=id)
		chat = await Chat.get(id=chat_id)
		
		await user.chats.remove(chat)
		logger.info(f"User with id: {id} removed from chat with id: {chat_id}.")
		
		if not await user.chats.exists():
			await user.delete()
			logger.info(f"User with id: {id} has no more chats, deleted.")
	except DoesNotExist:
		logger.error(f"User with id: {id} or chat with id: {chat_id} does not exist.")

async def get_user(id: int):
	try:
		logger.debug(f"Trying to get user with id: {id}")
		return await User.get(id=id)
	except DoesNotExist:
		logger.warning(f"User with id: {id} does not exist.")
		return None

async def get_mentions(chat_id: int):
	logger.debug(f"Fetching mentions for chat with id: {chat_id}")
	mentions = []
	
	try:
		chat = await Chat.get(id=chat_id).prefetch_related('users')
		users = await chat.users.all()

		for user in users:
			mentions.append(format_mention(user))
		
		logger.info(f"Fetched {len(mentions)} mentions for chat with id: {chat_id}.")
	except DoesNotExist:
		logger.error(f"Chat with id: {chat_id} does not exist.")
	
	return mentions
