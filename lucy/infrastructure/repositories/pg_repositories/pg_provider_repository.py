from lucy.application.repositories import ProviderRepository
from lucy.domain.models.provider import Provider

from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGProviderRepository(ProviderRepository):

    async def save(self, provider: Provider):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                    insert into providers (uuid, name, represent, phone, email, created_at, updated_at)
                    values ($1, $2, $3, $4, $5, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                provider.uuid,
                provider.name,
                provider.represent,
                provider.phone,
                provider.email
            )