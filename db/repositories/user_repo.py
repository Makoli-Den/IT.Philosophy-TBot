from db.models.user import User
from db.models.chat import Chat
from tortoise.exceptions import DoesNotExist
from utils.user_utils import format_mention

async def add_user(id: int, username: str, full_name: str, chat_id: int):
	try:
		user = await User.get(id=id)
	except DoesNotExist:
		user = await User.create(id=id, username=username, full_name=full_name)

	return user

async def remove_user(id: int, chat_id: int):
	try:
		user = await User.get(id=id)
		chat = await Chat.get(id=chat_id)
		
		await user.chats.remove(chat)
		
		if not await user.chats.exists():
			await user.delete()
	except DoesNotExist:
		pass

async def get_user(id: int):
	try:
		return await User.get(id=id)
	except DoesNotExist:
		return None

async def get_mentions(chat_id: int):
	mentions = []
	
	chat = await Chat.get(id=chat_id).prefetch_related('users')
	users = await chat.users.all()

	for user in users:
		mentions.append(format_mention(user))
	
	return mentions
