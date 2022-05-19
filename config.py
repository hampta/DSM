# -*- coding: utf-8 -*-
from os import getenv

# settings
TOKEN = getenv("TOKEN")
ADMIN_ID = getenv("ADMIN_ID") or 403972025133301760
DATABASE_URL = getenv("DATABASE_URL") or "sqlite://database.sqlite3"
WEBHOOK_URL = getenv("WEBHOOK_URL")
COMMAND_PREFIX = "!"
CRON_LOOP_INTERVAL = 60
CHECK_SERVER_INTERVAL = .7
CHECK_SERVER_INTERVAL_MAX = 6