from lucy.application.repositories import ProviderRepository
from lucy.application.use_case.brand_provider_use_case import BrandProviderUseCase
from lucy.domain.models.provider import Provider


class ProviderUseCase:

    def __init__(self, repository: ProviderRepository, brand_provider_use_case: BrandProviderUseCase = None, provider: Provider = None):
        self._repository = repository
        self._provider = provider
        self._brand_provider_use_case = brand_provider_use_case

    async def create(self):
        existing_provider = await self._repository.get_by_nit(self._provider.nit)
        if not existing_provider:
            new_provider = await self._repository.save(self._provider)
            return new_provider.to_dict() if new_provider else None
        return existing_provider.to_dict() if existing_provider else None

    async def get_all(self):
        providers_with_brands = await self._repository.get_all()
        result = []
        for entry in providers_with_brands:
            provider_dict = entry["provider"].to_dict()
            provider_dict["brands"] = [brand.to_dict() for brand in entry["brands"]]
            result.append(provider_dict)
        return result

    async def get_by_id(self, uuid):
        provider_with_brands = await self._repository.get_by_id(uuid)

        if not provider_with_brands:
            return None

        provider = provider_with_brands["provider"]
        brands = provider_with_brands["brands"]

        provider_dict = provider.to_dict()
        provider_dict["brands"] = [brand.to_dict() for brand in brands]

        return provider_dict

    async def update(self, uuid, update_data):
        provider = Provider(
            types_person=update_data.get('types_person'),
            nit=update_data.get('nit'),
            name=update_data.get('name'),
            represent=update_data.get('represent'),
            phone=update_data.get('phone'),
            email=update_data.get('email'),
            certificate_url=update_data.get('certificate_url', ''),
        )
        updated_provider = await self._repository.update(uuid, provider)

        if 'brands' in update_data:
            brands = update_data['brands']
            await self._brand_provider_use_case.update(uuid, brands)

        if updated_provider:
            provider_dict = updated_provider.to_dict()
            provider_dict['brands'] = update_data.get('brands', [])
            return provider_dict

        return None

    async def delete(self, uuid):
        deleted_provider = await self._repository.delete(uuid)
        return deleted_provider.to_dict() if deleted_provider else None
