from lucy.application.repositories import TechnicalSheetRepository
from lucy.domain.models.product import Product
from lucy.domain.models.technical_sheets import TechnicalSheet
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGTechnicalRepository(TechnicalSheetRepository):
    async def save(self, technical_sheet: TechnicalSheet, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                insert into technical_sheets 
                (uuid, documents, product_uuid, created_at, updated_at)
                values ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                technical_sheet.uuid,
                technical_sheet.documents,
                product.uuid
            )
