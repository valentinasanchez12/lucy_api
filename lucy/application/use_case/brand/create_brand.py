from lucy.application.repositories import BrandRepository
from lucy.domain.models.brand import Brand


class BrandUseCase:
    def __init__(self, repository: BrandRepository, brand: Brand = None):
        self._repository = repository
        self._brand = brand

    async def create(self):
        existing_brand = await self._repository.get_by_name(self._brand.name)
        if not existing_brand:
            brand = await self._repository.save(brand=self._brand)
            return brand.to_dict()
        return existing_brand.to_dict()

    async def get_all(self):
        brands = await self._repository.get_all()
        return [brand.to_dict() for brand in brands]

    async def get_by_id(self, uuid):
        brand = await self._repository.get_by_id(uuid=uuid)
        return brand.to_dict() if brand else None

    async def update(self, uuid, update_data):
        updated_brand = Brand(**update_data)
        brand = await self._repository.update(uuid=uuid, brand=updated_brand)
        return brand.to_dict() if brand else None

    async def delete(self, brand_id):
        deleted_brand = await self._repository.delete(brand_id)
        return deleted_brand.to_dict() if deleted_brand else None
