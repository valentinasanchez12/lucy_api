from lucy.application.repositories import BrandProviderRepository
from lucy.domain.models.brand import Brand
from lucy.domain.models.provider import Provider


class BrandProviderUseCase:
    def __init__(self, repository: BrandProviderRepository):
        self._repository = repository

    async def save(self, brands: [Brand], provider: Provider):
        for brand in brands:
            await self._repository.save(brand, provider)

    async def update(self, provider_id: str, brand_ids: list):
        await self._repository.update(provider_id, brand_ids)
