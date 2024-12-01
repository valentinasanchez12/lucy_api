from lucy.application.repositories import CharacteristicRepository
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGCharacteristicRepository(CharacteristicRepository):
    async def update(self, product_id: str, characteristics: Characteristic):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                # Elimina las características existentes
                await connection.execute(
                    '''
                    DELETE FROM characteristics WHERE product_id = $1
                    ''',
                    product_id
                )
                for characteristic in characteristics:
                    await connection.execute(
                        '''
                        INSERT INTO characteristics (uuid, product_id, characteristic, description, created_at)
                        VALUES (gen_random_uuid(), $1, $2, $3, LOCALTIMESTAMP)
                        ''',
                        product_id,
                        characteristic.characteristic,
                        characteristic.description
                    )

    async def save(self, characteristic: Characteristic, product_uuid):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                INSERT INTO characteristics (uuid, characteristic, description, product_id, created_at, updated_at)
                VALUES ($1, $2, $3, $4, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                characteristic.uuid,
                characteristic.characteristic,
                characteristic.description,
                product_uuid,
            )
