from aioredis import client

from src.infrastructure.abstract.singleton import AbstractSingletonInfrastructure
from src.utils.env_config import config


class RedisKeyDBInfrastructure(AbstractSingletonInfrastructure):
    @staticmethod
    async def _get_connection():
        connection_url = config("REDIS_CONNECTION_URL")
        redis_connection = client.Redis(host=connection_url)
        return redis_connection

