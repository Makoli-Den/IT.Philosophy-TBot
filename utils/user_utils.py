def format_mention(user):
	return f"[{user.username or user.first_name}](tg://user?id={user.id})"