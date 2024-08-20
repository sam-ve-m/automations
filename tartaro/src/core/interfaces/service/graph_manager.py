from abc import ABC, abstractmethod
from typing import Optional, Any, Callable


class InterfaceGraphManager(ABC):
    @classmethod
    @abstractmethod
    async def get_figure(cls, query: Optional[Any], done_callback: Callable):
        pass

    @classmethod
    @abstractmethod
    async def get_filtered_figure(cls, query: Any, filter_query: Any) -> str:
        pass
