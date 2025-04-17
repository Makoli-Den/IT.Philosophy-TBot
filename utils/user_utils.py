import logging

logger = logging.getLogger(__name__)

def format_mention(user):
	try:
		logger.debug(f"Attempting to format mention for user: {user.id}")
		
		mention = f"[{user.username or user.first_name}](tg://user?id={user.id})"
		
		logger.info(f"Successfully formatted mention for user: {user.id}")
		return mention
	except Exception as e:
		logger.error(f"Error occurred while formatting mention for user {user.id}: {str(e)}")
		raise
