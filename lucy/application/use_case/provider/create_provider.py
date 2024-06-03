from lucy.application.repositories import ProviderRepository
from lucy.domain.models.provider import Provider


class CreateProvider:

    def __init__(self, repository: ProviderRepository, provider: Provider):
        self._repository = repository
        self._provider = provider

    async def create(self):
        await self._repository.save(self._provider)