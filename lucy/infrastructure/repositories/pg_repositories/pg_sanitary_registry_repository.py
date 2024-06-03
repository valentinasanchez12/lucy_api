from lucy.application.repositories import SanitaryRegistryRepository
from lucy.domain.models.sanitary_registry import SanitaryRegistry

from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGSanitaryRegistryRepository(SanitaryRegistryRepository):

    async def save(self, sanitary_registry: SanitaryRegistry):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                    insert into sanitary_registry 
                    (uuid, documents, number_registry, expiration_date, cluster, status, type_risk, created_at, updated_at)
                    values ($1, $2, $3, $4, $5, $6, $7, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                sanitary_registry.uuid,
                sanitary_registry.documents,
                sanitary_registry.number_registry,
                sanitary_registry.expiration_date,
                sanitary_registry.cluster,
                sanitary_registry.status,
                sanitary_registry.type_risk
            )