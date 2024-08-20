from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.abstract.singleton import AbstractSingletonInfrastructure
from src.utils.env_config import config


class MongoDBInfrastructure(AbstractSingletonInfrastructure):
    @staticmethod
    async def _get_connection():
        connection_url = config("MONGO_CONNECTION_URL")
        mongo_connection = AsyncIOMotorClient(connection_url)
        return mongo_connection

