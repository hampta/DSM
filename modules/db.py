# -*- coding: utf-8 -*-
from tortoise import Tortoise
from tortoise.models import Model
from tortoise import fields
from os import getenv

# init db function for tortoise ORM or sqlite if not found in env variables (for testing)
async def init():
    if getenv("DATABASE_URL") is None:
        await Tortoise.init(
            db_url='sqlite://database.sqlite3',
            modules={'models': ['modules.db']}
        )
    else:
        await Tortoise.init(
            db_url=getenv("DATABASE_URL"),
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