from abc import ABCMeta, abstractmethod

from lucy.domain.models.category import Category
from lucy.domain.models.provider import Provider


class CategoryRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, category: Category):
        pass


class ProviderRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, provider: Provider):
        pass
