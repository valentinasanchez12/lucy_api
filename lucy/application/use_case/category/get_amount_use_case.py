from lucy.application.repositories import CategoryRepository


class GetAmountUseCase:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def get_amount(self):
        return await self.category_repository.get_amount()