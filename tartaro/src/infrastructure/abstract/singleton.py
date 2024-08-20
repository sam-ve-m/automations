from abc import ABC, abstractmethod
from typing import Any

from src.core.interfaces.infrastructure.i_infrastructure import InterfaceInfrastructure


class AbstractSingletonInfrastructure(InterfaceInfrastructure, ABC):
    connection: Any = None

    @classmethod
    async def get_singleton_connection(cls):
        if cls.connection is None:
            cls.connection = await cls._get_connection()
        return cls.connection

    @staticmethod
    @abstractmethod
    async def _get_connection():
        pass
