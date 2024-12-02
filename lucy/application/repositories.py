from abc import ABCMeta, abstractmethod

from lucy.domain.models.brand import Brand
from lucy.domain.models.category import Category
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.comments import Comments
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
    async def get_by_id(self, category_id: str):
        pass

    @abstractmethod
    async def update(self, category_id: str, category: Category):
        pass

    @abstractmethod
    async def delete(self, category_id: str):
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
    async def get_by_id(self, registry_id: str):
        pass

    @abstractmethod
    async def update(self, registry_id: str, sanitary_registry: SanitaryRegistry):
        pass

    @abstractmethod
    async def delete(self, registry_id: str):
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
    async def delete(self, brand_id: str):
        pass


class ProductRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, product: Product):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str):
        pass

    @abstractmethod
    async def update(self, product_id: str, product: Product, images: list):
        pass

    @abstractmethod
    async def delete(self, product_id: str):
        pass

    @abstractmethod
    async def search(self, query: str):
        pass

    @abstractmethod
    async def get_random(self, limit: int):
        pass


class CommentRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, comment: Comments, product_uuid):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, comment_id: str):
        pass

    @abstractmethod
    async def update(self, comment_id: str, product: Product):
        pass

    @abstractmethod
    async def delete(self, comment_id: str):
        pass

    @abstractmethod
    async def get_by_product_id(self, product_id: str):
        pass


class TechnicalSheetRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, technical_sheet: TechnicalSheet, product_uuid):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, uuid: str):
        pass

    @abstractmethod
    async def update(self, product_id: str, technical_sheet: TechnicalSheet):
        pass

    @abstractmethod
    async def delete(self, uuid: str):
        pass


class CharacteristicRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, characteristic: Characteristic, product_uuid):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str):
        pass

    @abstractmethod
    async def update(self, product_id: str, characteristics: list):
        pass

    @abstractmethod
    async def delete(self, product_id: str):
        pass


class BrandProviderRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, brand: Brand, provider: Provider):
        pass

    @abstractmethod
    async def update(self, provider_id: str, brands: list):
        pass
