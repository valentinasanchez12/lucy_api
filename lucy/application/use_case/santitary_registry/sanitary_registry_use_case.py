from lucy.application.repositories import SanitaryRegistryRepository
from lucy.domain.models.sanitary_registry import SanitaryRegistry


class SanitaryRegistryUseCase:

    def __init__(self, repository: SanitaryRegistryRepository, sanitary_registry: SanitaryRegistry = None):
        self._repository = repository
        self._sanitary_registry = sanitary_registry

    async def create(self):
        existing_registry = await self._repository.get_by_number_registry(self._sanitary_registry.number_registry)
        if not existing_registry:
            new_registry = await self._repository.save(self._sanitary_registry)
            return new_registry.to_dict() if new_registry else None
        return existing_registry.to_dict() if existing_registry else None

    async def get_all(self):
        sanitary_registries = await self._repository.get_all()
        return [registry.to_dict() for registry in sanitary_registries]

    async def get_by_id(self, registry_id: str):
        sanitary_registry = await self._repository.get_by_id(registry_id)
        return sanitary_registry.to_dict() if sanitary_registry else None

    async def update(self, registry_id: str, update_data: dict, static_url):
        sanitary_registry = SanitaryRegistry(
            uuid=registry_id,
            url=static_url,
            number_registry=update_data.get("number_registry"),
            expiration_date=update_data.get("expiration_date"),
            cluster=update_data.get("cluster"),
            status=update_data.get("status"),
            type_risk=update_data.get("type_risk"),
        )

        updated_registry = await self._repository.update(registry_id, sanitary_registry)
        return updated_registry.to_dict() if updated_registry else None

    async def delete(self, registry_id: str):
        deleted_registry = await self._repository.delete(registry_id)
        return deleted_registry.to_dict() if deleted_registry else None
