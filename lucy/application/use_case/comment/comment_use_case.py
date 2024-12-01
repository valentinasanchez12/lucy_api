from lucy.application.repositories import CommentRepository
from lucy.domain.models.comments import Comments


class CommentUseCase:
    def __init__(self, repository: CommentRepository):
        self._repository = repository

    async def create(self, comment: Comments, product_id: str):
        comment = await self._repository.save(comment, product_id)
        return comment.to_dict() if comment else None

    async def get_by_product_id(self, product_id: str):
        comments = await self._repository.get_by_product_id(product_id)
        return [comment.to_dict() for comment in comments]
