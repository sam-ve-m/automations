from abc import ABC, abstractmethod
from typing import Dict, Any, Coroutine

from src.repository.abstract.cache import AbstractCacheRepository
from src.services.abstract.graphs import AbstractGraph


class AbstractCollectionGraph(AbstractGraph, AbstractCacheRepository, ABC):
    def __init__(self, redis_infrastructure):
        self.cache_connection = redis_infrastructure

    @staticmethod
    @abstractmethod
    async def _build_graph_figures(query: Any) -> Dict[str, Coroutine]:
        pass

    @staticmethod
    @abstractmethod
    async def _build_filtered_figures(query: Any, filter_query: Any) -> str:
        pass

    @classmethod
    async def _update_html(cls, query):
        figures = await cls._build_graph_figures(query)
        return figures

    @classmethod
    async def _build_filter_option(cls, filter_cache_key: str, query: str, filter_query: Any):
        figure = await cls._build_filtered_figures(query, filter_query)
        cls.figures_html.update({filter_cache_key: figure})
