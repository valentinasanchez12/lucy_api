from lucy.application.repositories import TechnicalSheetRepository
from lucy.domain.models.product import Product
from lucy.domain.models.technical_sheets import TechnicalSheet
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGTechnicalSheetRepository(TechnicalSheetRepository):
    async def get_all(self):
        pass

    async def get_by_id(self, uuid: str):
        pass

    async def delete(self, uuid: str):
        pass

    async def update(self, product_id: str, technical_sheet: TechnicalSheet):
        pool = get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                existing_sheet = await connection.fetchval(
                    '''
                    SELECT document FROM technical_sheets WHERE product_id = $1
                    ''',
                    product_id
                )
                if not existing_sheet or existing_sheet != technical_sheet.document:
                    await connection.execute(
                        '''
                        DELETE FROM technical_sheets WHERE product_id = $1
                        ''',
                        product_id
                    )
                    await connection.execute(
                        '''
                        INSERT INTO technical_sheets (uuid, product_id, document, created_at, updated_at)
                        VALUES (gen_random_uuid(), $1, $2, LOCALTIMESTAMP, LOCALTIMESTAMP)
                        ''',
                        product_id,
                        technical_sheet.document
                    )

    async def save(self, technical_sheet: TechnicalSheet, product_uuid):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                INSERT INTO technical_sheets (uuid, document, product_id, created_at, updated_at)
                VALUES ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                technical_sheet.uuid,
                technical_sheet.document,
                product_uuid,
            )
