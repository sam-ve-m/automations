import asyncio
import json
import time
from enum import Enum
from typing import Dict

import orjson
from bokeh import layouts, models, embed

from src.core.enums.product_screens import QuoteTypes, QuoteTypesConstraints
from src.infrastructure.mongo import MongoDBInfrastructure
from src.infrastructure.redis import RedisKeyDBInfrastructure
from src.repository.collections_group_analysis import CollectionGroupRepository
from src.services.abstract.graph_creator import AbstractGraphCreator
from src.services.base.create_graphs import CreateGraph
from src.services.base.sample_callback import SampleCallback
from src.utils import async_auxiliary
from src.services.base.collection_graph import AbstractCollectionGraph


class ProductPage(AbstractCollectionGraph, SampleCallback, CreateGraph, AbstractGraphCreator):

    @staticmethod
    async def _build_graph_figures(product_page_name: str) -> Dict[str, str]:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        collections_repository = CollectionGroupRepository(mongo_infrastructure, redis_infrastructure)
        product_pages = QuoteTypes.__members__
        pages_graphs = {
            page_name: ProductPage._create_product_page_figure_html(page_name, page_sections, collections_repository)
            for page_name, page_sections in product_pages.items()
        }
        return pages_graphs

    @staticmethod
    async def _build_filtered_figures(product_page_name: str, raw_filter_query: dict) -> str:
        mongo_infrastructure = await MongoDBInfrastructure.get_singleton_connection()
        redis_infrastructure = await RedisKeyDBInfrastructure.get_singleton_connection()
        collection_group_repository = CollectionGroupRepository(mongo_infrastructure, redis_infrastructure)
        page_sections = QuoteTypes[product_page_name]
        filter_query = await ProductPage._build_filter_query(
            page_sections,
            raw_filter_query,
            collection_group_repository
        )
        page_graphs = await ProductPage._create_product_page_figure(
            product_page_name, page_sections, collection_group_repository, filter_query
        )
        filter_text = []
        for section, fields in raw_filter_query.items():
            filter_text += [
                f"{section}-{field} {'covered' if exists else 'missing'}"
                for field, exists in fields.items()
            ]
        filter_text = f"Actual filter: {'none' if not filter_text else ', '.join(filter_text)}."
        layout = layouts.column(models.PreText(text=filter_text), page_graphs)
        return "".join(embed.components(layout))

    @staticmethod
    async def _build_filter_query(
            page_sections: Enum,
            filter_query: dict,
            collection_group_repository: CollectionGroupRepository,
    ) -> dict:
        collections = []
        filter_fields = {}
        for section, fields in filter_query.items():
            quote_type_page = page_sections.value
            collections += quote_type_page[section].value
            filter_fields.update({
                f'object.{field}': {'$exists': existence}
                for field, existence in fields.items()
            })
        pages_filtered_tickers = await collection_group_repository.identify_tickers_in_filter(collections, filter_fields)
        page_constraint = QuoteTypesConstraints[page_sections.name].value
        tickers = pages_filtered_tickers.get(page_constraint, [None])
        return {"_id": {"$in": tickers}}

    @staticmethod
    async def _create_product_page_figure(
            page_name: str,
            page_sections: Enum,
            collection_group_repository: CollectionGroupRepository,
            filter_query: dict = {},
    ) -> models.LayoutDOM:
        pages_sections = page_sections.value.__members__
        quote_type_constraint = QuoteTypesConstraints[page_name].value
        page_graphs = {
            section_name: ProductPage._create_product_page_section_figure(
                collections.value,
                section_name,
                quote_type_constraint,
                collection_group_repository,
                filter_query
            ) for section_name, collections in pages_sections.items()
        }
        page_graphs = await async_auxiliary.gather_dict_values(page_graphs)
        page_figures = layouts.column(*page_graphs.values())
        return page_figures

    @staticmethod
    async def _create_product_page_figure_html(
            page_name: str,
            page_sections: Enum,
            collection_group_repository: CollectionGroupRepository,
            filter_query: dict = {},
    ) -> str:
        page_figures = await ProductPage._create_product_page_figure(
            page_name,
            page_sections,
            collection_group_repository,
            filter_query,
        )
        return "".join(embed.components(page_figures))

    @staticmethod
    async def _create_product_page_section_figure(
            collections: list,
            section_name: str,
            constraint: str,
            collection_group_repository: CollectionGroupRepository,
            filter_query: dict
    ) -> models.Model:
        if not collections:
            return layouts.column()
        grouped_tickers = await collection_group_repository.identify_collections_tickers(collections, filter_query)
        raw_quote_type_fields = grouped_tickers.get(constraint, {})
        quote_type_fields = {
            field: [await ProductPage._pretty_dumps_dict(ticker) for ticker in value]
            async for field, value, in ProductPage._async_read_dict_items(raw_quote_type_fields)
        }
        layout = await ProductPage._create_figure(quote_type_fields, section_name)
        return layout

    dumps_methods = {
        dict: lambda x, y, z: f"{x}: {asyncio.get_event_loop().run_until_complete(ProductPage._pretty_dumps_dict(y, z))}",
        list: lambda x, y, z: f"{x}-{','.join(map(str, y))};",
    }

    @staticmethod
    async def _pretty_dumps_dict(dictionary: dict, default=None):
        pretty_dumps = ""
        for key, value in dictionary.items():
            dumps_method = ProductPage.dumps_methods.get(type(value), lambda x, y, z: f"{x}: {y};" if x != y else x)
            pretty = dumps_method(key, value, default)
            pretty_dumps += pretty
        if not pretty_dumps:
            return default
        return pretty_dumps

    @staticmethod
    async def _async_read_dict_items(Sadasdas):
        for field, value, in Sadasdas.items():
            yield field, value
