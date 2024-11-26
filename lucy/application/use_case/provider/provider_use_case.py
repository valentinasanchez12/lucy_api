from lucy.application.repositories import ProviderRepository
from lucy.domain.models.provider import Provider


class ProviderUseCase:

    def __init__(self, repository: ProviderRepository, provider: Provider = None):
        self._repository = repository
        self._provider = provider

    async def create(self):
        provider = await self._repository.save(self._provider)
        return provider.to_dict() if provider else None

    async def get_all(self):
        providers = await self._repository.get_all()
        return [provider.to_dict() for provider in providers]

    async def get_by_id(self, uuid):
        provider = await self._repository.get_by_id(uuid)
        return provider.to_dict() if provider else None

    async def update(self, uuid, update_data):
        provider = Provider(
            name=update_data['name'],
            represent=update_data['represent'],
            phone=update_data['phone'],
            email=update_data['email'],
        )
        updated_provider = await self._repository.update(uuid, provider)
        return updated_provider.to_dict() if updated_provider else None

    async def delete(self, uuid):
        delete_provider = await self._repository.delete(uuid)
        return delete_provider.to_dict() if delete_provider else None
