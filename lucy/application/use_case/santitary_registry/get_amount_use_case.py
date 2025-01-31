from lucy.application.repositories import SanitaryRegistryRepository


class GetAmountUseCase:
    def __init__(self, repository: SanitaryRegistryRepository):
        self.repository = repository

    async def get_amount(self):
        return await self.repository.get_amount()