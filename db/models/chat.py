from tortoise import fields, models
from tortoise.fields.relational import ManyToManyRelation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from db.models.user import User

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