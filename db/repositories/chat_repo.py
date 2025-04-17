from db.models.chat import Chat
from tortoise.exceptions import DoesNotExist

async def add_chat(id: int, title: str):
	try:
		await Chat.get(id=id)
	except DoesNotExist:
		await Chat.create(id=id, title=title)

async def get_chat(id: int):
	try:
		return await Chat.get(id=id)
	except DoesNotExist:
		return None

async def get_chats():
	return await Chat.all()

async def add_user_to_chat(user_id: int, chat_id: int):
	from db.models.user import User
	
	try:
		user = await User.get(id=user_id)
		chat = await Chat.get(id=chat_id)
		await user.chats.add(chat)
	except DoesNotExist:
		pass

async def remove_user_from_chat(user_id: int, chat_id: int):
	from db.models.user import User
	
	try:
		user = await User.get(id=user_id)
		chat = await Chat.get(id=chat_id)
		await user.chats.remove(chat)
	except DoesNotExist:
		pass
