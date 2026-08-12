from assets.dtos import (
    BrandCreateDTO,
    BrandUpdateDTO,
)
from assets.models import Brand
from assets.repositories import BrandRepository


class BrandService:

    def __init__(self):
        self.repository = BrandRepository()

    def create(
        self,
        dto: BrandCreateDTO,
    ) -> Brand:
        """
        Create a new Brand.
        """

        brand = Brand(
            country=dto.country,
            name=dto.name,
            description=dto.description,
        )

        return self.repository.create(brand)

    def update(
        self,
        brand: Brand,
        dto: BrandUpdateDTO,
    ) -> Brand:
        """
        Update an existing Brand.
        """

        brand.country = dto.country
        brand.name = dto.name
        brand.description = dto.description
        brand.is_active = dto.is_active

        return self.repository.update(brand)

    def delete(
        self,
        brand: Brand,
    ):
        """
        Delete a Brand.
        """

        self.repository.delete(brand)