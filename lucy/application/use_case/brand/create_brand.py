from lucy.application.repositories import BrandRepository
from lucy.domain.models.brand import Brand


class CreateBrand:
    def __init__(self, repository: BrandRepository, brand: Brand):
        self._repository = repository
        self._brand = brand

    async def create(self):
        try:
            await self._repository.save(brand=self._brand)
        except ValueError as e:
            return 500, False, str(e)
        return 200, True, 'Created brand successfully'
