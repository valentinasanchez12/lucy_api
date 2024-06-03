from lucy.application.repositories import CategoryRepository
from lucy.domain.models.category import Category


class CreateCategory:

    def __init__(self, repository: CategoryRepository, category: Category):
        self._repository = repository
        self._category = category

    async def create(self):
        await self._repository.save(self._category)
