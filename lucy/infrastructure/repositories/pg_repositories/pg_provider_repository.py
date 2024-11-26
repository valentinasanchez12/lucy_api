from lucy.application.repositories import ProviderRepository
from lucy.domain.models.provider import Provider
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGProviderRepository(ProviderRepository):

    async def save(self, provider: Provider):
        pool = get_pool()
        async with pool.acquire() as connection:
            inserted_row = await connection.fetchrow(
                '''
                    insert into providers (uuid, name, represent, phone, email, created_at, updated_at)
                    values ($1, $2, $3, $4, $5, LOCALTIMESTAMP, LOCALTIMESTAMP)
                    returning uuid, name, represent, phone, email, created_at, updated_at
                ''',
                provider.uuid,
                provider.name,
                provider.represent,
                provider.phone,
                provider.email
            )
            return Provider(
                uuid=inserted_row['uuid'],
                name=inserted_row['name'],
                represent=inserted_row['represent'],
                phone=inserted_row['phone'],
                email=inserted_row['email'],
                created_at=inserted_row['created_at'],
            )

    async def get_all(self):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT uuid, name, represent, phone, email, created_at, updated_at, delete_at
                FROM providers WHERE delete_at IS NULL
                '''
            )
            return [Provider(
                uuid=row['uuid'],
                name=row['name'],
                represent=row['represent'],
                phone=row['phone'],
                email=row['email'],
                created_at=row['created_at'],
                update_at=row['updated_at'],
                delete_at=row['delete_at']
            ) for row in rows]

    async def get_by_id(self, uuid: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, name, represent, phone, email, created_at, updated_at, delete_at
                FROM providers
                WHERE uuid = $1 AND delete_at IS NULL
                ''',
                uuid
            )
            if row:
                return Provider(
                    uuid=row['uuid'],
                    name=row['name'],
                    represent=row['represent'],
                    phone=row['phone'],
                    email=row['email'],
                    created_at=row['created_at'],
                    update_at=row['updated_at'],
                    delete_at=row['delete_at']
                )
            return None

    async def update(self, uuid: str, provider: Provider):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE providers
                SET name = COALESCE($2, name),
                    represent = COALESCE($3, represent),
                    phone = COALESCE($4, phone),
                    email = COALESCE($5, email),
                    updated_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND delete_at IS NULL
                RETURNING uuid, name, represent, phone, email, created_at, updated_at, delete_at
                ''',
                uuid,
                provider.name,
                provider.represent,
                provider.phone,
                provider.email
            )
            if row:
                return Provider(
                    uuid=row['uuid'],
                    name=row['name'],
                    represent=row['represent'],
                    phone=row['phone'],
                    email=row['email'],
                    created_at=row['created_at'],
                    update_at=row['updated_at'],
                    delete_at=row['delete_at']
                )
            return None

    async def delete(self, uuid: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE providers
                SET delete_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND delete_at IS NULL
                RETURNING uuid, name, represent, phone, email, created_at, updated_at, delete_at
                ''',
                uuid
            )
            if row:
                return Provider(
                    uuid=row['uuid'],
                    name=row['name'],
                    represent=row['represent'],
                    phone=row['phone'],
                    email=row['email'],
                    created_at=row['created_at'],
                    update_at=row['updated_at'],
                    delete_at=row['delete_at']
                )
            return None
