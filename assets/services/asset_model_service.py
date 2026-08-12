from assets.dtos import (
    AssetModelCreateDTO,
    AssetModelUpdateDTO,
)
from assets.models import AssetModel
from assets.repositories import AssetModelRepository


class AssetModelService:

    def __init__(self):
        self.repository = AssetModelRepository()

    def create(
        self,
        dto: AssetModelCreateDTO,
    ) -> AssetModel:
        """
        Create a new Asset Model.
        """

        asset_model = AssetModel(
            country=dto.country,
            category=dto.category,
            brand=dto.brand,
            name=dto.name,
            manufacturer_part_number=dto.manufacturer_part_number,
            technical_specifications=dto.technical_specifications,
            description=dto.description,
        )

        return self.repository.create(asset_model)

    def update(
        self,
        asset_model: AssetModel,
        dto: AssetModelUpdateDTO,
    ) -> AssetModel:
        """
        Update an existing Asset Model.
        """

        asset_model.country = dto.country
        asset_model.category = dto.category
        asset_model.brand = dto.brand
        asset_model.name = dto.name
        asset_model.manufacturer_part_number = dto.manufacturer_part_number
        asset_model.technical_specifications = dto.technical_specifications
        asset_model.description = dto.description
        asset_model.is_active = dto.is_active

        return self.repository.update(asset_model)

    def delete(
        self,
        asset_model: AssetModel,
    ):
        """
        Delete an Asset Model.
        """

        self.repository.delete(asset_model)