from django.db.models import query
from django.urls import reverse

from core.dtos import BreadcrumbDTO, PageDTO
from core.dtos.toolbar import Toolbar, ToolbarButton
from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder

from organizations.forms import CompanyCreateForm, CompanyUpdateForm, company
from organizations.repositories import CompanyRepository
from organizations.services import CompanyService


class CompanyPageService:

    def __init__(self):
        self.service = CompanyService()
        self.repository = CompanyRepository()

    def list_page(self, query: str = "",  page=1) -> PageDTO:

        companies = self.repository.list(
            query=query,
            page=page
        )

        grid = (
            DataGridBuilder("Companies")
            .selectable(False)
            .column(
                field="code",
                label="Code",
            )
            .column(
                field="name",
                label="Company",
            )
            .column(
                field="country",
                label="Country",
            )
            .column(
                field="phone",
                label="Phone",
            )
            .column(
                field="email",
                label="Email",
            )
            .column(
                field="is_active",
                label="Status",
            )
            .action(
                title="View company",
                icon="bi-eye",
                url_name="organizations:company-detail",
                css_class="grid-action grid-action--view",
            )
            .action(
                title="Edit company",
                icon="bi-pencil-square",
                url_name="organizations:company-edit",
                css_class="grid-action grid-action--edit",
            )
            .action(
                title="Delete company",
                icon="bi-trash",
                url_name="organizations:company-delete",
                css_class="grid-action grid-action--delete",
                method="POST",
                confirm_message="Delete this company? This action cannot be undone.",
            )
            .search(
        url=reverse("organizations:company-list"),
        query=query,
        placeholder="Search companies...",
    )
        )

        for company in companies.object_list:
            grid.row(
                row_id=company.id,
                code=company.code,
                name=company.name,
                country=company.country.name,
                phone=company.phone,
                email=company.email,
                is_active=company.is_active,
            )

        grid.paginate(companies)

        return PageDTO(
            title="Companies",
            subtitle="Manage organization companies",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Companies",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New company",
                        icon="bi-plus-lg",
                        url=reverse("organizations:company-create"),
                        style="warning",
                    ),
                ],
            ),
            content=grid.build(),
        )

    def create_page(self, form=None) -> PageDTO:

        form = form or CompanyCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Company",
                form=form,
            )

            .section("General Information")
                .field("name", width=6)
                .field("country", width=6)
                .field("legal_name", width=6)
                .field("registration_number", width=6)
                .field("tax_number", width=6)

            .section("Contact Information")
                .field("phone", width=6)
                .field("email", width=6)
                .field("website", width=12)

            .section("Additional Information")
                .field("logo", width=12)
                .field("description", width=12)

            .submit("Save", icon="bi-check-circle")
            .cancel(reverse("organizations:company-list"))

            .build()
        )

        return PageDTO(
            title="Create Company",
            subtitle="Register a new company",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Companies",
                    url=reverse("organizations:company-list"),
                ),
                BreadcrumbDTO(
                    label="Create",
                ),
            ],
            content=form_dto,
        )

    def edit_page(self, company, form=None) -> PageDTO:
        form = form or CompanyUpdateForm(instance=company)

        form_dto = (
            FormBuilder(
                title=f"Edit {company.name}",
                form=form,
            )
            .section("Company information")
                .field("name", width=6)
                .field("country", width=6)
                .field("legal_name", width=6)
                .field("registration_number", width=6)
                .field("tax_number", width=6)
            .section("Contact information")
                .field("phone", width=6)
                .field("email", width=6)
                .field("website", width=12)
            .section("Additional information")
                .field("logo", width=12)
                .field("description", width=12)
            .submit("Save changes", icon="bi-check-circle")
            .cancel(reverse("organizations:company-list"))
            .build()
        )

        return PageDTO(
            title=f"Edit {company.name}",
            subtitle=company.code,
            breadcrumb=[
                BreadcrumbDTO(label="Organizations", url="/organizations/"),
                BreadcrumbDTO(label="Companies", url=reverse("organizations:company-list")),
                BreadcrumbDTO(label="Edit"),
            ],
            content=form_dto,
        )


    def detail_page(self, company_id):

        company = self.repository.get(company_id)

        return PageDTO(
            title=company.name,
            subtitle=company.code,
        )
