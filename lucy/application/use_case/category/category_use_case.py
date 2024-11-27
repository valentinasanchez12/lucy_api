from lucy.application.repositories import CategoryRepository
from lucy.domain.models.category import Category


class CategoryUseCase:

    def __init__(self, repository: CategoryRepository, category: Category = None):
        self._repository = repository
        self._category = category

    async def create(self):
        category = await self._repository.save(category=self._category)
        return category.to_dict()

    async def get_all(self):
        categories = await self._repository.get_all()
        return [category.to_dict() for category in categories]

    async def get_by_id(self, category_id):
        category = await self._repository.get_by_id(category_id=category_id)
        return category.to_dict() if category else None

    async def update(self, category_id, category_data):
        updated_category = Category(**category_data)
        category = await self._repository.update(category_id=category_id, category=updated_category)
        return category.to_dict() if category else None

    async def delete(self, category_id):
        deleted_category = await self._repository.delete(category_id=category_id)
        return deleted_category.to_dict() if deleted_category else None

