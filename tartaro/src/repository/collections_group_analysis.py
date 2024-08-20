from pymongo.database import Database

from src.core.dto.graph import GraphSample
from src.core.static.pipeline.aggregate_fields import AggregateFields
from src.core.static.pipeline.get_filter_ids import GetFilteredIds
from src.core.static.pipeline.suply_excel import SupplyExcel
from src.repository.abstract.cache import AbstractCacheRepository, async_cached_operation
from src.repository.abstract.mongo import AbstractMongoCRUDRepository
from src.utils.env_config import config


class CollectionGroupRepository(AbstractMongoCRUDRepository, AbstractCacheRepository):
    database_name = config("MONGO_DATABASE_ANALYSIS")
    collection_name = config("MONGO_COLLECTION_IDENTIFIERS")

    def __init__(
            self,
            mongo_infrastructure,
            redis_infrastructure
    ):
        self.cache_connection = redis_infrastructure
        database: Database = mongo_infrastructure[self.database_name]
        self.collection = database[self.collection_name]

    @async_cached_operation(ttl_in_seconds=600)
    async def identify_collections_tickers(self, collections_names: list, filter_query: dict) -> dict:
        mongo_pipeline_commands = await AggregateFields.get_pipeline(collections_names, filter_query)
        identified_tickers = await self.aggregate(mongo_pipeline_commands)
        quote_types_fields = {
            str(quote_type.get("_id")): quote_type.get("fields")
            async for quote_type in identified_tickers
        }
        return quote_types_fields

    @async_cached_operation(ttl_in_seconds=180)
    async def identify_tickers_in_filter(self, collections_names: list, filter_query: dict) -> dict:
        mongo_pipeline_commands = await GetFilteredIds.get_pipeline(collections_names, filter_query)
        identified_tickers = await self.aggregate(mongo_pipeline_commands)
        quote_types_fields = {
            str(quote_type.get("_id")): quote_type.get("tickers")
            async for quote_type in identified_tickers
        }
        return quote_types_fields

    @async_cached_operation(ttl_in_seconds=180)
    async def top_tickers_sample(self, collections_names: list, filter_query: dict, top_symbols: list) -> GraphSample:
        # filter_query.update({"_id:": {"$in": top_symbols}}) TODO: Enquanto não houver uma fonte para os top symbols
        mongo_pipeline_commands = await SupplyExcel.get_pipeline(collections_names, filter_query)
        distinct_keys_pipeline = mongo_pipeline_commands + await SupplyExcel.get_distinct_keys_pipeline()
        sample_possible_fields = [key.get("_id") async for key in await self.aggregate(distinct_keys_pipeline)]
        sample_possible_fields.sort()
        sample_tickers_cursor = await self.aggregate(mongo_pipeline_commands)
        sample_tickers = await sample_tickers_cursor.to_list(None)
        return GraphSample(
            sample=sample_tickers,
            possible_fields=sample_possible_fields,
        )
