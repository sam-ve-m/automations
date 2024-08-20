import asyncio
from abc import ABC, abstractmethod
from asyncio import Future
from typing import Dict, Any, Callable, Coroutine

from src.core.interfaces.service.graph_manager import InterfaceGraphManager
from src.utils import async_auxiliary
from src.utils.async_auxiliary import application_loop


class AbstractGraph(InterfaceGraphManager, ABC):
    figures_html: Dict[str, str] = {}
    is_idle: asyncio.Lock = None

    @classmethod
    @abstractmethod
    async def _update_html(cls, query) -> dict:
        pass

    @classmethod
    @abstractmethod
    async def _build_filter_option(cls, filter_cache_key: str, query: str, filter_query: Any):
        pass

    @classmethod
    async def get_figure(cls, query: Any, done_callback: Callable):
        await cls._set_lock()
        async with cls.is_idle:
            if not cls.figures_html:
                await cls._create_figure_html(query, done_callback)
            else:
                wanted_result = cls.figures_html.get(query, await cls._not_found_message(query))
                await done_callback(wanted_result)

    @classmethod
    async def _create_figure_html(cls, query: Any, done_callback: Callable):
        figures: Dict[str, Coroutine] = await cls._update_html(query)
        if query not in figures:
            await done_callback(await cls._not_found_message(query))
            cls.figures_html = await async_auxiliary.gather_dict_values(figures)
        else:
            figure_future = figures.pop(query)
            figure = await figure_future
            await done_callback(figure)
            cls.figures_html = await async_auxiliary.gather_dict_values(figures)
            cls.figures_html.update({query: figure})

    @classmethod
    async def get_filtered_figure(cls, query: str, filter_query: Any) -> str:
        filter_cache_key = query if not filter_query else ":".join((query, str(filter_query)))
        if not cls.figures_html.get(filter_cache_key):
            await cls._build_filter_option(filter_cache_key, query, filter_query)
        return cls.figures_html.get(filter_cache_key)

    @staticmethod
    async def _not_found_message(query: str):
        return f'Not found: {query}'

    @classmethod
    async def _set_lock(cls):
        if not cls.is_idle:
            cls.is_idle = asyncio.Lock(loop=asyncio.get_running_loop())

