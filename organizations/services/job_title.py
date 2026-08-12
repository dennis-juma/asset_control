from organizations.dtos import (
    JobTitleCreateDTO,
    JobTitleUpdateDTO,
)
from organizations.models import JobTitle
from organizations.repositories.job_title import JobTitleRepository


class JobTitleService:

    def __init__(self):
        self.repository = JobTitleRepository()

    def create_job_title(
        self,
        dto: JobTitleCreateDTO,
    ) -> JobTitle:

        job_title = JobTitle(
            country_id=dto.country,
            department_id=dto.department,
            name=dto.name,
            description=dto.description,
        )

        return self.repository.create(
            job_title,
        )

    def update_job_title(
        self,
        job_title: JobTitle,
        dto: JobTitleUpdateDTO,
    ) -> JobTitle:

        job_title.country_id = dto.country
        job_title.department_id = dto.department
        job_title.name = dto.name
        job_title.description = dto.description
        job_title.is_active = dto.is_active

        return self.repository.update(
            job_title,
        )

    def delete(
        self,
        job_title: JobTitle,
    ):

        return self.repository.delete(
            job_title,
        )