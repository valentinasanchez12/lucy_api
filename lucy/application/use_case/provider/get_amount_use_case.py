class GetAmountUseCase:
    def __init__(self, provider_repository):
        self.provider_repository = provider_repository

    async def get_amount(self):
        return await self.provider_repository.get_amount()