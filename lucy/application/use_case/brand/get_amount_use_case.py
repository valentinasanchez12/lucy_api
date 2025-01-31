class GetAmountUseCase:
    def __init__(self, brand_repository):
        self._brand_repository = brand_repository

    def execute(self):
        return self._brand_repository.get_amount()
