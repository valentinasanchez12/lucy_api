from lucy.application.repositories import CategoryRepository
from lucy.domain.models.category import Category
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGCategoryRepository(CategoryRepository):

    async def save(self, category: Category):
        pool = get_pool()
        async with pool.acquire() as connection:
            await connection.execute(
                '''
                    insert into categories (uuid, name, created_at, updated_at)
                    values ($1, $2, LOCALTIMESTAMP, LOCALTIMESTAMP)
                ''',
                category.uuid,
                category.name
            )
