# -*- coding: utf-8 -*-
from config import DATABASE_URL
from tortoise import Tortoise, fields
from tortoise.models import Model


# init db function 
async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['modules.db']}
    )
    await Tortoise.generate_schemas()

# server model for DB
class Servers(Model):
    id = fields.IntField(pk=True)
    worked = fields.BooleanField(default=True)
    author = fields.BigIntField()
    channel = fields.BigIntField()
    message = fields.BigIntField()
    ip = fields.CharField(max_length=16)
    port = fields.SmallIntField()
    name = fields.CharField(max_length=255, default="")
    game = fields.CharField(max_length=255, default="")
    latest_updated = fields.DatetimeField(auto_now_add=True)
