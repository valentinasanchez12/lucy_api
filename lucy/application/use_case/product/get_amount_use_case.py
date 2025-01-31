from lucy.application.repositories import ProductRepository


class GetAmountUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_amount(self):
        return await self.repository.get_amount()