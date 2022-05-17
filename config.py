# -*- coding: utf-8 -*-
from os import getenv

# settings
TOKEN = getenv("TOKEN")
ADMIN_ID = getenv("ADMIN_ID") or 403972025133301760
WEBHOOK_URL = getenv("WEBHOOK_URL")
COMMAND_PREFIX = "!"