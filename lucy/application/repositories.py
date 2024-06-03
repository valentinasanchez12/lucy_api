from abc import ABCMeta, abstractmethod

from lucy.domain.models.category import Category


class CategoryRepository(metaclass=ABCMeta):

    @abstractmethod
    async def save(self, category: Category):
        pass
