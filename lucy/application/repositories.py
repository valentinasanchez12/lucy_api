from abc import ABCMeta, abstractmethod

from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.provider import Provider
from lucy.domain.models.sanitary_registry import SanitaryRegistry


class CategoryRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, category: Category):
        pass


class ProviderRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, provider: Provider):
        pass


class SanitaryRegistryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, sanitary_registry: SanitaryRegistry):
        pass


class BrandRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, brand: Brand):
        pass
