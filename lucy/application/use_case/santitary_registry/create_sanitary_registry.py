from lucy.application.repositories import SanitaryRegistryRepository
from lucy.domain.models.sanitary_registry import SanitaryRegistry


class CreateSanitaryRegistry:

    def __init__(self, repository: SanitaryRegistryRepository, sanitary_registry: SanitaryRegistry):
        self._repository = repository
        self._sanitary_registry = sanitary_registry

    async def create(self):
        await self._repository.save(self._sanitary_registry)