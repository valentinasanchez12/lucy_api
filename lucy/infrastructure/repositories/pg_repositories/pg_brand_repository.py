from lucy.application.repositories import BrandRepository
from lucy.domain.models.brand import Brand
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGBrandRepository(BrandRepository):
    async def get_all(self) -> [Brand]:
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM brands
                WHERE deleted_at IS NULL
                '''
            )
            return [Brand(
                uuid=row['uuid'],
                name=row['name'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                deleted_at=row['deleted_at']
            ) for row in rows]

    async def get_by_id(self, uuid: str) -> Brand:
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM brands
                WHERE uuid = $1 AND deleted_at IS NULL
                ''',
                uuid
            )
            if row:
                return Brand(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def update(self, uuid: str, brand: Brand) -> Brand:
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE brands
                SET name = COALESCE($2, name),
                    updated_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, name, created_at, updated_at, deleted_at
                ''',
                uuid,
                brand.name
            )
            if row:
                return Brand(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def delete(self, brand_id: str) -> Brand:
            pool = get_pool()
            async with pool.acquire() as connection:
                row = await connection.fetchrow(
                    '''
                    UPDATE brands
                    SET deleted_at = LOCALTIMESTAMP
                    WHERE uuid = $1 AND deleted_at IS NULL
                    RETURNING uuid, name, created_at, updated_at, deleted_at
                    ''',
                    brand_id
                )
                if row:
                    return Brand(
                        uuid=row['uuid'],
                        name=row['name'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        deleted_at=row['deleted_at']
                    )
                return None

    async def save(self, brand: Brand) -> Brand:
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                    insert into brands (uuid, name, created_at, updated_at)
                    values ($1, $2, LOCALTIMESTAMP, LOCALTIMESTAMP)
                    returning uuid, name, created_at, updated_at
                ''',
                brand.uuid,
                brand.name
            )
            return Brand(
                uuid=row['uuid'],
                name=row['name'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )

    async def get_by_name(self, name: str) -> Brand:
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM brands
                WHERE name = $1 AND deleted_at IS NULL
                ''',
                name
            )
            if row:
                return Brand(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None
