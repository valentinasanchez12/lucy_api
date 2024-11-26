from lucy.application.repositories import ProductRepository
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGProductRepository(ProductRepository):
    async def get_all(self):
        pass

    async def save(self, product: Product):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                insert into products
                (uuid, generic_name, commercial_name, description, measurement,
                formulation, composition, reference, use, status, sanitize_method, image,
                brand_uuid, category_uuid, sanitary_registry_uuid, created_at, _update_at)
                values
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                product.uuid,
                product.generic_name,
                product.commercial_name,
                product.description,
                product.measurement,
                product.formulation,
                product.composition,
                product.reference,
                product.use,
                product.status,
                product.sanitize_method,
                product.image,
                product.brand.uuid,
                product.category.uuid,
                product.sanitary_registry.uuid
            )
