from asyncpg import ForeignKeyViolationError

from lucy.application.repositories import BrandRepository
from lucy.domain.models.brand import Brand
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGBrandRepository(BrandRepository):
    async def save(self, brand: Brand):
        pool = get_pool()
        async with pool.acquire() as connection:
            try:
                await connection.execute(
                    '''
                        insert into brands (uuid, name, provider_uuid, created_at, updated_at)
                        values ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                    ''',
                    brand.uuid,
                    brand.name,
                    brand.provider.uuid
                )
            except ForeignKeyViolationError:
                raise ValueError('violates foreign key constraint')
