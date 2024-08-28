from lucy.application.repositories import CharacteristicRepository
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGCharacteristicRepository(CharacteristicRepository):
    async def save(self, characteristic: Characteristic, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                insert into characteristics 
                (uuid, characteristics, description, product_uuid, created_at, updated_at)
                values ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                characteristic.uuid,
                characteristic.characteristic,
                characteristic.description,
                product.uuid
            )
