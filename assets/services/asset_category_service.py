from assets.dtos import (
    AssetCategoryCreateDTO,
    AssetCategoryUpdateDTO,
)
from assets.models.asset_category import AssetCategory
from assets.repositories import AssetCategoryRepository


class AssetCategoryService:

    def __init__(self):
        self.repository = AssetCategoryRepository()

    def create(self, dto):
        category = AssetCategory(
            company=dto.company,
            parent=dto.parent,
            name=dto.name,
            description=dto.description,
            sort_order=dto.sort_order,
        )

        return self.repository.create(category)

    def update(
        self,
        category,
        dto,
    ):
        category.company = dto.company
        category.parent = dto.parent
        category.name = dto.name
        category.description = dto.description
        category.sort_order = dto.sort_order
        category.is_active = dto.is_active

        return self.repository.update(category)