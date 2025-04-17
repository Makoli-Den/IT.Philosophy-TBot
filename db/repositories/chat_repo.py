import logging
from db.models.chat import Chat
from tortoise.exceptions import DoesNotExist

logger = logging.getLogger(__name__)

async def add_chat(id: int, title: str):
	try:
		logger.debug(f"Trying to get chat with id: {id}")
		await Chat.get(id=id)
		logger.info(f"Chat with id: {id} already exists.")
	except DoesNotExist:
		logger.info(f"Chat with id: {id} does not exist, creating new one.")
		await Chat.create(id=id, title=title)
		logger.info(f"Chat with id: {id} created successfully.")

async def get_chat(id: int):
	try:
		logger.debug(f"Trying to get chat with id: {id}")
		return await Chat.get(id=id)
	except DoesNotExist:
		logger.warning(f"Chat with id: {id} does not exist.")
		return None

async def get_chats():
	logger.debug("Fetching all chats.")
	return await Chat.all()

async def add_user_to_chat(user_id: int, chat_id: int):
	from db.models.user import User
	
	try:
		logger.debug(f"Trying to add user with id: {user_id} to chat with id: {chat_id}")
		user = await User.get(id=user_id)
		chat = await Chat.get(id=chat_id)
		await user.chats.add(chat)
		logger.info(f"User with id: {user_id} added to chat with id: {chat_id}.")
	except DoesNotExist:
		logger.error(f"User with id: {user_id} or chat with id: {chat_id} does not exist.")

async def remove_user_from_chat(user_id: int, chat_id: int):
	from db.models.user import User
	
	try:
		logger.debug(f"Trying to remove user with id: {user_id} from chat with id: {chat_id}")
		user = await User.get(id=user_id)
		chat = await Chat.get(id=chat_id)
		await user.chats.remove(chat)
		logger.info(f"User with id: {user_id} removed from chat with id: {chat_id}.")
	except DoesNotExist:
		logger.error(f"User with id: {user_id} or chat with id: {chat_id} does not exist.")
