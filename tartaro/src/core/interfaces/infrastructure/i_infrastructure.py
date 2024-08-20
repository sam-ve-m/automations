from abc import ABC, abstractmethod


class InterfaceInfrastructure(ABC):
    @classmethod
    @abstractmethod
    async def get_singleton_connection(cls):
        pass
