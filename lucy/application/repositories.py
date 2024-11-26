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

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, category: Category):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class ProviderRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, provider: Provider):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, provider: Provider):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class SanitaryRegistryRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, sanitary_registry: SanitaryRegistry):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, provider: Provider):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class BrandRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, brand: Brand):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, brand: Brand):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class ProductRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, product: Product):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, product: Product):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class ObservationRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, observation: Observation, product: Product):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, product: Product):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class TechnicalSheetRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, technical_sheet: TechnicalSheet, product: Product):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, technical_sheet: TechnicalSheet):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class CharacteristicRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, characteristic: Characteristic, product: Product):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, uuid: str, characteristic: Characteristic):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass
