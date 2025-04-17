from tortoise import fields, models
from tortoise.fields.relational import ManyToManyRelation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from db.models.chat import Chat

class User(models.Model):
	id = fields.IntField(pk=True)
	username = fields.CharField(max_length=64, null=True)
	full_name = fields.CharField(max_length=128, null=True)

	chats: ManyToManyRelation["Chat"]

	class Meta:
		table = "user"
		
	def __str__(self):
		return self.username or self.full_name
