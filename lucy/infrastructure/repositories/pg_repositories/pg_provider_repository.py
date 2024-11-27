from lucy.application.repositories import ProviderRepository
from lucy.domain.models.brand import Brand
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
                SELECT 
                    p.uuid AS provider_uuid,
                    p.name AS provider_name,
                    p.represent,
                    p.phone,
                    p.email,
                    p.created_at AS provider_created_at,
                    p.updated_at AS provider_updated_at,
                    p.delete_at AS provider_delete_at,
                    b.uuid AS brand_uuid,
                    b.name AS brand_name,
                    b.created_at AS brand_created_at,
                    b.updated_at AS brand_updated_at,
                    b.delete_at AS brand_delete_at
                FROM providers p
                LEFT JOIN brand_providers bp ON p.uuid = bp.provider_uuid
                LEFT JOIN brands b ON bp.brand_uuid = b.uuid
                WHERE p.delete_at IS NULL
                '''
            )

            providers_dict = {}
            for row in rows:
                provider_id = row['provider_uuid']

                if provider_id not in providers_dict:
                    providers_dict[provider_id] = {
                        "provider": Provider(
                            uuid=row['provider_uuid'],
                            name=row['provider_name'],
                            represent=row['represent'],
                            phone=row['phone'],
                            email=row['email'],
                            created_at=row['provider_created_at'],
                            update_at=row['provider_updated_at'],
                            delete_at=row['provider_delete_at']
                        ),
                        "brands": []
                    }

                if row['brand_uuid']:
                    brand = Brand(
                        uuid=row['brand_uuid'],
                        name=row['brand_name'],
                        created_at=row['brand_created_at'],
                        update_at=row['brand_updated_at'],
                        delete_at=row['brand_delete_at']
                    )
                    providers_dict[provider_id]["brands"].append(brand)

            return [
                {
                    "provider": providers_dict[provider_id]["provider"],
                    "brands": providers_dict[provider_id]["brands"]
                }
                for provider_id in providers_dict
            ]

    async def get_by_id(self, uuid: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT 
                    p.uuid AS provider_uuid,
                    p.name AS provider_name,
                    p.represent,
                    p.phone,
                    p.email,
                    p.created_at AS provider_created_at,
                    p.updated_at AS provider_updated_at,
                    p.delete_at AS provider_delete_at,
                    b.uuid AS brand_uuid,
                    b.name AS brand_name,
                    b.created_at AS brand_created_at,
                    b.updated_at AS brand_updated_at,
                    b.delete_at AS brand_delete_at
                FROM providers p
                LEFT JOIN brand_providers bp ON p.uuid = bp.provider_uuid
                LEFT JOIN brands b ON bp.brand_uuid = b.uuid
                WHERE p.uuid = $1 AND p.delete_at IS NULL
                ''',
                uuid
            )

            if not rows:
                return None

            provider_data = None
            brands = []

            for row in rows:
                if provider_data is None:
                    provider_data = Provider(
                        uuid=row['provider_uuid'],
                        name=row['provider_name'],
                        represent=row['represent'],
                        phone=row['phone'],
                        email=row['email'],
                        created_at=row['provider_created_at'],
                        update_at=row['provider_updated_at'],
                        delete_at=row['provider_delete_at']
                    )

                if row['brand_uuid']:
                    brands.append(Brand(
                        uuid=row['brand_uuid'],
                        name=row['brand_name'],
                        created_at=row['brand_created_at'],
                        update_at=row['brand_updated_at'],
                        delete_at=row['brand_delete_at']
                    ))

            return {
                "provider": provider_data,
                "brands": brands
            }

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
            async with connection.transaction():
                await connection.execute(
                    '''
                    DELETE FROM brand_providers
                    WHERE provider_uuid = $1
                    ''',
                    uuid
                )
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
