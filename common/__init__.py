# -*- coding:UTF-8 -*-

from redis import Redis

from Demo import settings

rds = Redis(**settings.REDIS)


