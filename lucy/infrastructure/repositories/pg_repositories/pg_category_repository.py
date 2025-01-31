import uuid

from lucy.application.repositories import CategoryRepository
from lucy.domain.models.category import Category
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGCategoryRepository(CategoryRepository):

    async def get_all(self):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM categories
                WHERE deleted_at IS NULL
                '''
            )
            return [Category(
                uuid=row['uuid'],
                name=row['name'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                deleted_at=row['deleted_at']
            ) for row in rows]

    async def get_by_id(self, category_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM categories
                WHERE uuid = $1 AND deleted_at IS NULL
                ''',
                category_id
            )
            if row:
                return Category(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def update(self, category_id: str, category: Category):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE categories
                SET name = COALESCE($2, name),
                    updated_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, name, created_at, updated_at, deleted_at
                ''',
                category_id,
                category._name
            )
            if row:
                return Category(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def delete(self, category_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                UPDATE categories
                SET deleted_at = LOCALTIMESTAMP
                WHERE uuid = $1 AND deleted_at IS NULL
                RETURNING uuid, name, created_at, updated_at, deleted_at
                ''',
                category_id
            )
            if row:
                return Category(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None

    async def save(self, category: Category):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                    insert into categories (uuid, name, created_at, updated_at)
                    values ($1, $2, LOCALTIMESTAMP, LOCALTIMESTAMP)
                    returning uuid, name, created_at, updated_at
                ''',
                category.uuid,
                category.name
            )
        return Category(
            uuid=row['uuid'],
            name=row['name'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )

    async def get_by_name(self, name: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                SELECT uuid, name, created_at, updated_at, deleted_at
                FROM categories
                WHERE name = $1 AND deleted_at IS NULL
                ''',
                name
            )
            if row:
                return Category(
                    uuid=row['uuid'],
                    name=row['name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    deleted_at=row['deleted_at']
                )
            return None
