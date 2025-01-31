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
                    insert into providers (uuid, types_person, nit, name, represent, phone, email, created_at, updated_at)
                    values ($1, $2, $3, $4, $5, $6,$7, LOCALTIMESTAMP, LOCALTIMESTAMP)
                    returning uuid, types_person, nit, name, represent, phone, email, created_at, updated_at
                ''',
                provider.uuid,
                provider.types_person,
                provider.nit,
                provider.name,
                provider.represent,
                provider.phone,
                provider.email
            )
            return Provider(
                uuid=inserted_row['uuid'],
                types_person=inserted_row['types_person'],
                nit=inserted_row['nit'],
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
                    p.types_person,
                    p.nit,
                    p.name AS provider_name,
                    p.represent,
                    p.phone,
                    p.email,
                    p.created_at AS provider_created_at,
                    p.updated_at AS provider_updated_at,
                    p.deleted_at AS provider_deleted_at,
                    b.uuid AS brand_uuid,
                    b.name AS brand_name,
                    b.created_at AS brand_created_at,
                    b.updated_at AS brand_updated_at,
                    b.deleted_at AS brand_deleted_at
                FROM providers p
                LEFT JOIN brand_providers bp ON p.uuid = bp.provider_uuid
                LEFT JOIN brands b ON bp.brand_uuid = b.uuid
                WHERE p.deleted_at IS NULL
                '''
            )

            providers_dict = {}
            for row in rows:
                provider_id = row['provider_uuid']

                if provider_id not in providers_dict:
                    providers_dict[provider_id] = {
                        "provider": Provider(
                            uuid=row['provider_uuid'],
                            types_person=row['types_person'],
                            nit=row['nit'],
                            name=row['provider_name'],
                            represent=row['represent'],
                            phone=row['phone'],
                            email=row['email'],
                            created_at=row['provider_created_at'],
                            updated_at=row['provider_updated_at'],
                            deleted_at=row['provider_deleted_at']
                        ),
                        "brands": []
                    }

                if row['brand_uuid']:
                    brand = Brand(
                        uuid=row['brand_uuid'],
                        name=row['brand_name'],
                        created_at=row['brand_created_at'],
                        updated_at=row['brand_updated_at'],
                        deleted_at=row['brand_deleted_at']
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
                    p.types_person,
                    p.nit,
                    p.name AS provider_name,
                    p.represent,
                    p.phone,
                    p.email,
                    p.created_at AS provider_created_at,
                    p.updated_at AS provider_updated_at,
                    p.deleted_at AS provider_deleted_at,
                    b.uuid AS brand_uuid,
                    b.name AS brand_name,
                    b.created_at AS brand_created_at,
                    b.updated_at AS brand_updated_at,
                    b.deleted_at AS brand_deleted_at
                FROM providers p
                LEFT JOIN brand_providers bp ON p.uuid = bp.provider_uuid
                LEFT JOIN brands b ON bp.brand_uuid = b.uuid
                WHERE p.uuid = $1 AND p.deleted_at IS NULL
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
                        types_person=row['types_person'],
                        nit=row['nit'],
                        name=row['provider_name'],
                        represent=row['represent'],
                        phone=row['phone'],
                        email=row['email'],
                        created_at=row['provider_created_at'],
                        updated_at=row['provider_updated_at'],
                        deleted_at=row['provider_deleted_at']
                    )

                if row['brand_uuid']:
                    brands.append(Brand(
                        uuid=row['brand_uuid'],
                        name=row['brand_name'],
                        created_at=row['brand_created_at'],
                        updated_at=row['brand_updated_at'],
                        deleted_at=row['brand_deleted_at']
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
                    types_person = COALESCE($3, types_person),
                    nit = COALESCE($4, nit),
                    represent = COALESCE($5, represent),
                    phone = COALESCE($6, phone),
                    email = COALESCE($7, email),
                    updated_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, nit, types_person, name, represent, phone, email, created_at, updated_at, deleted_at
                ''',
                uuid,
                provider.name,
                provider.types_person,
                provider.nit,
                provider.represent,
                provider.phone,
                provider.email
            )
            if row:
                return Provider(
                    uuid=row['uuid'],
                    name=row['name'],
                    types_person=row['types_person'],
                    nit=row['nit'],
                    represent=row['represent'],
                    phone=row['phone'],
                    email=row['email'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def delete(self, uuid: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                row = await connection.fetchrow(
                    '''
                    UPDATE providers
                    SET deleted_at = LOCALTIMESTAMP
                    WHERE uuid = $1 AND deleted_at IS NULL
                    RETURNING uuid, types_person, nit, name, represent, phone, email, created_at, updated_at, deleted_at
                    ''',
                    uuid
                )
                if row:
                    return Provider(
                        uuid=row['uuid'],
                        name=row['name'],
                        types_person=row['types_person'],
                        nit=row['nit'],
                        represent=row['represent'],
                        phone=row['phone'],
                        email=row['email'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        deleted_at=row['deleted_at']
                    )
                return None

    async def get_by_nit(self, nit: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT 
                    p.uuid AS provider_uuid,
                    p.types_person,
                    p.nit,
                    p.name AS provider_name,
                    p.represent,
                    p.phone,
                    p.email,
                    p.created_at AS provider_created_at,
                    p.updated_at AS provider_updated_at,
                    p.deleted_at AS provider_deleted_at
                FROM providers p
                WHERE p.nit = $1 AND p.deleted_at IS NULL
                ''',
                nit
            )

            if not row:
                return None
            return Provider(
                uuid=row['provider_uuid'],
                types_person=row['types_person'],
                nit=row['nit'],
                name=row['provider_name'],
                represent=row['represent'],
                phone=row['phone'],
                email=row['email'],
                created_at=row['provider_created_at'],
                updated_at=row['provider_updated_at'],
                deleted_at=row['provider_deleted_at']
            )

