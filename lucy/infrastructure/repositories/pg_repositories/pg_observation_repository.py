from lucy.application.repositories import ObservationRepository
from lucy.domain.models.observation import Observation
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGObservationRepository(ObservationRepository):
    async def save(self, observation: Observation, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                insert into observations 
                (uuid, observation, product_uuid, created_at, updated_at)
                values ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                observation.uuid,
                observation.observation,
                product.uuid
            )
