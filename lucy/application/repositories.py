from abc import ABCMeta, abstractmethod

from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.observation import Observation
from lucy.domain.models.product import Product
from lucy.domain.models.provider import Provider
from lucy.domain.models.sanitary_registry import SanitaryRegistry
from lucy.domain.models.technical_sheets import TechnicalSheet


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


class ProductRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, product: Product):
        pass

    @abstractmethod
    async def all_products(self):
        pass


class ObservationRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, observation: Observation, product: Product):
        pass


class TechnicalSheetRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, technical_sheet: TechnicalSheet, product: Product):
        pass


class CharacteristicRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, characteristic: Characteristic, product: Product):
        pass
