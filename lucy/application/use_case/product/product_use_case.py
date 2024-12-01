from lucy.application.repositories import ProductRepository, CommentRepository, CharacteristicRepository, \
    TechnicalSheetRepository


class ProductUseCase:
    def __init__(
            self,
            product_repository: ProductRepository,
            comment_repository: CommentRepository = None,
            characteristic_repository: CharacteristicRepository = None,
            technical_sheet_repository: TechnicalSheetRepository = None
    ):
        self._product_repository = product_repository
        self._comment_repository = comment_repository
        self._characteristic_repository = characteristic_repository
        self._technical_sheet_repository = technical_sheet_repository

    async def create(self, product, comment, characteristics, technical_sheet):
        saved_product = await self._product_repository.save(product)

        if not saved_product:
            raise ValueError("Failed to save product")

        if comment:
            await self._comment_repository.save(comment, product.uuid)

        for characteristic in characteristics:
            await self._characteristic_repository.save(characteristic, product.uuid)

        if technical_sheet:
            await self._technical_sheet_repository.save(technical_sheet, product.uuid)

        return saved_product.to_dict()

    async def get_by_id(self, product_id: str):
        product = await self._product_repository.get_by_id(product_id)
        return product.to_dict() if product else None

    async def update(self, product_id, product_data, images, characteristics, technical_sheet):
        updated_product = await self._product_repository.update(
            product_id=product_id,
            product=product_data,
            images=images
        )

        if not updated_product:
            raise ValueError("Product not found or cannot be updated.")

        await self._characteristic_repository.update(
            product_id=product_id,
            characteristics=characteristics
        )

        if technical_sheet:
            await self._technical_sheet_repository.update(
                product_id=product_id,
                technical_sheet=technical_sheet
            )

        return updated_product.to_dict()

    async def search(self, query: str):
        return await self._product_repository.search(query)

    async def get_random(self, limit: int = 12):
        return await self._product_repository.get_random(limit)
