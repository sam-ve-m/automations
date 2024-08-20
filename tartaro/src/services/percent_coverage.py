from typing import Dict

from bokeh import models, layouts, embed

from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure
from src.repository.data_base_analysis import MongoDatabaseRepository
from src.services.base.collection_graph import AbstractCollectionGraph
from src.services.base.create_graphs import CreateGraph
from src.services.base.sample_callback import SampleCallback


class FieldsCoverage(AbstractCollectionGraph, SampleCallback, CreateGraph):
    @staticmethod
    async def _build_graph_figures(collection_name: str) -> Dict[str, str]:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)
        collections_coverage = await repository.missing_fields()
        collections_graphs = {
            collection: FieldsCoverage._create_coverage_figure(coverage, collection)
            for collection, coverage in collections_coverage.items()
        }
        return collections_graphs

    @staticmethod
    async def _build_filtered_figures(collection_name: str, filter_queries: dict) -> str:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        repository = MongoDatabaseRepository(mongo_infrastructure, redis_infrastructure)
        filter_text_args = [
            f"{field} {'covered' if is_covered else 'missing'}"
            for field, is_covered in filter_queries.items()
        ]
        filter_coverage = await repository.missing_fields_in_filter(collection_name, filter_queries)
        figure = await FieldsCoverage._create_figure(filter_coverage, collection_name)
        filter_text = f"Actual filter: {'none' if not filter_text_args else ', '.join(filter_text_args)}."
        layout = layouts.column(models.PreText(text=filter_text), figure)
        return "".join(embed.components(layout))

    @staticmethod
    async def _create_coverage_figure(coverage: dict, collection: str) -> str:
        figure = await FieldsCoverage._create_figure(coverage, collection)
        figure_html = "".join(embed.components(figure))
        return figure_html
