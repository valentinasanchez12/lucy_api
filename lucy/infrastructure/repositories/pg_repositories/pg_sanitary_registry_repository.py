from lucy.application.repositories import SanitaryRegistryRepository
from lucy.domain.models.sanitary_registry import SanitaryRegistry

from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGSanitaryRegistryRepository(SanitaryRegistryRepository):

    async def get_all(self):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT uuid, url, number_registry, expiration_date, cluster, 
                status, type_risk, created_at, updated_at, deleted_at
                FROM sanitary_registry
                WHERE deleted_at IS NULL
                '''
            )
            return [
                SanitaryRegistry(
                    uuid=row['uuid'],
                    url=row['url'],
                    number_registry=row['number_registry'],
                    expiration_date=row['expiration_date'],
                    cluster=row['cluster'],
                    status=row['status'],
                    type_risk=row['type_risk'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at'],
                )
                for row in rows
            ]

    async def get_by_id(self, registry_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, url, number_registry, expiration_date, cluster, 
                status, type_risk, created_at, updated_at, deleted_at
                FROM sanitary_registry
                WHERE uuid = $1 AND deleted_at IS NULL
                ''',
                registry_id
            )
            if row:
                return SanitaryRegistry(
                    uuid=row['uuid'],
                    url=row['url'],
                    number_registry=row['number_registry'],
                    expiration_date=row['expiration_date'],
                    cluster=row['cluster'],
                    status=row['status'],
                    type_risk=row['type_risk'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at'],
                )
            return None

    async def update(self, registry_id: str, sanitary_registry: SanitaryRegistry):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE sanitary_registry
                SET
                    url = COALESCE($2, url),
                    number_registry = COALESCE($3, number_registry),
                    expiration_date = COALESCE($4, expiration_date),
                    cluster = COALESCE($5, cluster),
                    status = COALESCE($6, status),
                    type_risk = COALESCE($7, type_risk),
                    updated_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, url, number_registry, expiration_date, cluster, 
                status, type_risk, created_at, updated_at, deleted_at
                ''',
                registry_id,
                sanitary_registry.url,
                sanitary_registry.number_registry,
                sanitary_registry.expiration_date,
                sanitary_registry.cluster,
                sanitary_registry.status,
                sanitary_registry.type_risk,
            )
            if row:
                return SanitaryRegistry(
                    uuid=row['uuid'],
                    url=row['url'],
                    number_registry=row['number_registry'],
                    expiration_date=row['expiration_date'],
                    cluster=row['cluster'],
                    status=row['status'],
                    type_risk=row['type_risk'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at'],
                )
            return None

    async def delete(self, registry_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE sanitary_registry
                SET deleted_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, url, number_registry, expiration_date, cluster, 
                status, type_risk, created_at, updated_at, deleted_at
                ''',
                registry_id
            )
            if row:
                return SanitaryRegistry(
                    uuid=row['uuid'],
                    url=row['url'],
                    number_registry=row['number_registry'],
                    expiration_date=row['expiration_date'],
                    cluster=row['cluster'],
                    status=row['status'],
                    type_risk=row['type_risk'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at'],
                )
            return None

    async def save(self, sanitary_registry: SanitaryRegistry):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                INSERT INTO sanitary_registry
                (uuid, url, number_registry, expiration_date, cluster, status, type_risk, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, LOCALTIMESTAMP, LOCALTIMESTAMP)
                RETURNING uuid, url, number_registry, expiration_date, cluster, status, type_risk, created_at, updated_at
                ''',
                sanitary_registry.uuid,
                sanitary_registry.url,
                sanitary_registry.number_registry,
                sanitary_registry.expiration_date,
                sanitary_registry.cluster,
                sanitary_registry.status,
                sanitary_registry.type_risk
            )
            if row:
                return SanitaryRegistry(
                    uuid=row['uuid'],
                    url=row['url'],
                    number_registry=row['number_registry'],
                    expiration_date=row['expiration_date'],
                    cluster=row['cluster'],
                    status=row['status'],
                    type_risk=row['type_risk'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=None
                )
            return None
