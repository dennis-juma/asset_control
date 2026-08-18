from organizations.dtos import (
    DepartmentCreateDTO,
    DepartmentUpdateDTO,
)
from organizations.models import (
    Country,
    Department,
   
)


class DepartmentService:

    def create_department(
        self,
        dto: DepartmentCreateDTO,
    ):

        country = Country.objects.get(
            pk=dto.country,
        )

        parent = None

        if dto.parent:
            parent = Department.objects.get(
                pk=dto.parent,
            )

        return Department.objects.create(
            country=country,
            parent=parent,
            name=dto.name,
            cost_center=dto.cost_center,
            description=dto.description,
        )

    def update_department(
        self,
        department,
        dto: DepartmentUpdateDTO,
    ):

        department.country = Country.objects.get(
            pk=dto.country,
        )


        department.parent = (
            Department.objects.get(pk=dto.parent)
            if dto.parent
            else None
        )

        department.name = dto.name
        department.cost_center = dto.cost_center
        department.description = dto.description
        department.is_active = dto.is_active

        department.save()

        return department

    def delete(
        self,
        department,
    ):
        department.delete()