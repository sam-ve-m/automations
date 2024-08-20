from src.core.enums.product_screens import QuoteTypes, QuoteTypesConstraints
from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure
from src.repository.collections_group_analysis import CollectionGroupRepository
from src.repository.data_base_analysis import MongoDatabaseRepository
from src.repository.excel_transformation import ExcelTransformation


class ToExcelFileService:
    @staticmethod
    async def get_ticker_excel(ticker: str) -> bytes:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)

        if not (ticker_details_json := await repository.find_ticker_by_id(ticker.upper())):
            return bytes()
        transformation_repository = ExcelTransformation(redis_infrastructure)
        excel_file_bytes = await transformation_repository.get_ticker_excel_file(ticker_details_json)
        return excel_file_bytes

    @staticmethod
    async def get_collection_group_excel(product_page: str, page_section: str, highlights: dict) -> bytes:
        top_symbols = []  # TODO: Encontrar uma fonte para os top symbols, por enquanto essa função está desabilitada
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = CollectionGroupRepository(mongo_infrastructure, redis_infrastructure)

        filter_query = {"object."+field: {"$exists": exists} for field, exists in highlights.items()}
        quote_type_constraint = QuoteTypesConstraints[product_page].value
        filter_query.update({"object.constraint": quote_type_constraint})
        quote_type = QuoteTypes[product_page].value
        collections = quote_type[page_section].value

        if not (filter_coverage := await repository.top_tickers_sample(collections, filter_query, top_symbols)):
            return bytes()
        transformation_repository = ExcelTransformation(redis_infrastructure)
        excel_file_bytes = await transformation_repository.get_graph_excel_file(page_section, filter_coverage)
        return excel_file_bytes

    @staticmethod
    async def get_collection_excel(collection: str, highlights: dict) -> bytes:
        top_symbols = []  # TODO: Encontrar uma fonte para os top symbols, por enquanto essa função está desabilitada
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)

        filter_query = {field: {"$exists": exists} for field, exists in highlights.items()}
        if not (filter_coverage := await repository.top_tickers_sample(collection, filter_query, top_symbols)):
            return bytes()
        transformation_repository = ExcelTransformation(redis_infrastructure)
        excel_file_bytes = await transformation_repository.get_graph_excel_file(collection, filter_coverage)
        return excel_file_bytes
