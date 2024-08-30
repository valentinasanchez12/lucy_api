from lucy.application.repositories import ProductRepository, ObservationRepository, CharacteristicRepository, \
    TechnicalSheetRepository
from lucy.domain.models.characteristic import Characteristic
from lucy.domain.models.observation import Observation
from lucy.domain.models.product import Product
from lucy.domain.models.technical_sheets import TechnicalSheet


class CreateProduct:
    def __init__(
            self,
            product_repository: ProductRepository,
            observation_repository: ObservationRepository,
            characteristic_repository: CharacteristicRepository,
            technical_sheet_repository: TechnicalSheetRepository,
            product: Product,
            observation: [Observation],
            technical_sheet: [TechnicalSheet],
            characteristic: [Characteristic],
    ):
        self._product = product
        self._observation = observation
        self._technical_sheet = technical_sheet
        self._characteristic = characteristic
        self._product_repository = product_repository
        self._observation_repository = observation_repository
        self._characteristic_repository = characteristic_repository
        self._technical_sheet_repository = technical_sheet_repository

    async def create(self):
        await self._product_repository.save(self._product)
        await self._observation_repository.save(self._observation, self._product)
        await self._characteristic_repository.save(self._characteristic, self._product)
        await self._technical_sheet_repository.save(self._technical_sheet, self._product)
