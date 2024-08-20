from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure
from src.repository.data_base_analysis import MongoDatabaseRepository


class TickerUpdate:
    @staticmethod
    async def update_ticker(ticker_update: dict) -> dict:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)
        collections_updates_status = await repository.update_ticker_collections(ticker_update)
        return collections_updates_status
