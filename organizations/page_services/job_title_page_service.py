from django.urls import reverse
from organizations.repositories.job_title import JobTitleRepository
from organizations.services.job_title import JobTitleService

from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)

from core.dtos.toolbar import (
    Toolbar,
    ToolbarButton,
)

from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder

from organizations.forms.job_title import (
    JobTitleCreateForm,
    JobTitleUpdateForm,
)


class JobTitlePageService:

    def __init__(self):

        self.service = JobTitleService()

        self.repository = JobTitleRepository()


    def list_page(
    self,
    query="",
    page=1,
) -> PageDTO:

        job_titles = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Job Titles")

        grid.column(field="code", label="Code")
        grid.column(field="name", label="Job Title")
        grid.column(field="company", label="Company")
        grid.column(field="department", label="Department")
        grid.column(field="is_active", label="Status")

        for job in job_titles:

            grid.row(
                row_id=job.id,
                code=job.code,
                name=job.name,
                company=job.company.name,
                department=job.department.name,
                is_active=job.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="organizations:job-title-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="organizations:job-title-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="organizations:job-title-delete",
        )

        grid.paginate(job_titles)

        return PageDTO(
            title="Job Titles",
            subtitle="Manage job titles",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Job Titles",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New Job Title",
                        icon="bi-plus-lg",
                        url=reverse(
                            "organizations:job-title-create",
                        ),
                        style="warning",
                    ),
                ],
            ),
            content=grid.build(),
        )
    def create_page(self):

        form = JobTitleCreateForm()

        form_dto = (

            FormBuilder(
                title="Create Job Title",
                form=form,
            )

            .section("General Information")

            .field("company", 6)
            .field("department", 6)

            .field("name", 12)

            .section("Description")

            .field("description", 12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "organizations:job-title-list",
            )

            .build()

        )

        return PageDTO(

            title="Create Job Title",

            subtitle="Register a new job title",

            breadcrumb=[

                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),

                BreadcrumbDTO(
                    label="Job Titles",
                    url=reverse(
                        "organizations:job-title-list",
                    ),
                ),

                BreadcrumbDTO(
                    label="Create",
                ),

            ],

            content=form_dto,

        )


    def detail_page(
    self,
    job_title,
):

        form = JobTitleUpdateForm(
            instance=job_title,
        )

        for field in form.fields.values():
            field.disabled = True

        form_dto = (

            FormBuilder(
                title="Job Title Details",
                form=form,
            )

            .section("General Information")

            .field("company", 6)
            .field("department", 6)

            .field("name", 12)

            .section("Description")

            .field("description", 12)

            .reverse(
                "organizations:job-title-list",
            )

            .build()

        )

        return PageDTO(

            title="Job Title Details",

            subtitle=job_title.name,

            breadcrumb=[

                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),

                BreadcrumbDTO(
                    label="Job Titles",
                    url=reverse(
                        "organizations:job-title-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=job_title.name,
                ),

            ],

            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "organizations:job-title-update",
                            kwargs={
                                "pk": job_title.id,
                            },
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "organizations:job-title-list",
                        ),
                        style="secondary",
                    ),
                ],
            ),

            content=form_dto,

        )


    def update_page(
    self,
    job_title,
):

        form = JobTitleUpdateForm(
            instance=job_title,
        )

        form_dto = (

            FormBuilder(
                title="Edit Job Title",
                form=form,
            )

            .section("General Information")

            .field("company", 6)
            .field("department", 6)

            .field("name", 12)

            .section("Description")

            .field("description", 12)

            .section("Status")

            .field("is_active", 12)

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "organizations:job-title-list",
            )

            .build()

        )

        return PageDTO(

            title="Edit Job Title",

            subtitle=job_title.name,

            breadcrumb=[

                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),

                BreadcrumbDTO(
                    label="Job Titles",
                    url=reverse(
                        "organizations:job-title-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=job_title.name,
                    url=reverse(
                        "organizations:job-title-detail",
                        args=[job_title.pk],
                    ),
                ),

                BreadcrumbDTO(
                    label="Edit",
                ),

            ],

            content=form_dto,

        )
