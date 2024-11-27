from lucy.application.repositories import BrandProviderRepository
from lucy.domain.models.brand import Brand
from lucy.domain.models.provider import Provider
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGBrandProviderRepository(BrandProviderRepository):
    async def update(self, provider_id: str, brands: list):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    '''
                    DELETE FROM brand_providers
                    WHERE provider_uuid = $1
                    ''',
                    provider_id
                )
                for brand_id in brands:
                    await connection.execute(
                        '''
                        INSERT INTO brand_providers (brand_uuid, provider_uuid)
                        VALUES ($1, $2)
                        ''',
                        brand_id,
                        provider_id
                    )

    async def save(self, brand: Brand, provider: Provider):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.fetchrow(
                '''
                insert into brand_provider (brand_uuid, provider_uuid)
                values ($1, $2)
                ''',
                brand.uuid,
                provider.uuid
            )
