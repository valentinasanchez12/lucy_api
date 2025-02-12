from lucy.application.repositories import CommentRepository
from lucy.domain.models.comments import Comments
from lucy.domain.models.product import Product
from lucy.infrastructure.repositories.pg_repositories.pg_pool import get_pool


class PGCommentRepository(CommentRepository):

    async def get_by_product_id(self, product_id: str):
        pool = get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                '''
                SELECT uuid, comment, product_id, created_at, updated_at
                FROM comments
                WHERE product_id = $1 AND deleted_at IS NULL
                ORDER BY created_at DESC
                ''',
                product_id
            )
            return [
                Comments(
                    uuid=row["uuid"],
                    comment=row["comment"],
                    product={"uuid": row["product_id"]},
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
                for row in rows
            ]

    async def get_all(self):
        pass

    async def get_by_id(self, comment_id: str):
        pass

    async def update(self, comment_id: str, product: Product):
        pass

    async def delete(self, comment_id: str):
        pass

    async def save(self, comment: Comments, product_uuid):
        pool = get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                '''
                INSERT INTO comments (uuid, comment, product_id, created_at, updated_at)
                VALUES ($1, $2, $3, LOCALTIMESTAMP, LOCALTIMESTAMP)
                RETURNING uuid, comment, product_id, created_at, updated_at
                ''',
                comment.uuid,
                comment.comment,
                product_uuid,
            )
            print(row['comment'])
            if row:
                return Comments(
                    uuid=row["uuid"],
                    comment=row["comment"],
                    product_uuid=row["product_id"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
