from lucy.application.repositories import SanitaryRegistryRepository
from lucy.domain.models.sanitary_registry import SanitaryRegistry


class SanitaryRegistryUseCase:

    def __init__(self, repository: SanitaryRegistryRepository, sanitary_registry: SanitaryRegistry = None):
        self._repository = repository
        self._sanitary_registry = sanitary_registry

    async def create(self):
        inserted_registry = await self._repository.save(sanitary_registry=self._sanitary_registry)
        return inserted_registry.to_dic() if inserted_registry else None

    async def get_all(self):
        sanitary_registries = await self._repository.get_all()
        return [registry.to_dict() for registry in sanitary_registries]

    async def get_by_id(self, registry_id: str):
        sanitary_registry = await self._repository.get_by_id(registry_id)
        return sanitary_registry.to_dict() if sanitary_registry else None

    async def update(self, registry_id: str, update_data: dict, file_service):
        file_path = None

        if "file_name" in update_data and "file_content" in update_data:
            file_path = file_service.upload_file(update_data["file_name"], update_data["file_content"])

        sanitary_registry = SanitaryRegistry(
            uuid=registry_id,
            url=file_path,
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
