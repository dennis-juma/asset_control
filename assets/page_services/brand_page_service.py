from django.urls import reverse

from assets.repositories.brand_repository import BrandRepository
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

from assets.forms import (
    BrandCreateForm,
    BrandUpdateForm,
)
from assets.repositories import BrandRepository


class BrandPageService:

    def __init__(self):
        self.repository = BrandRepository()

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
        self,
        query="",
        page=1,
    ) -> PageDTO:

        brands = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Brands")

        grid.column(
            field="code",
            label="Code",
        )

        grid.column(
            field="name",
            label="Brand",
        )


        grid.column(
            field="company",
            label="Company",
        )


        grid.column(
            field="is_active",
            label="Status",
        )

        for brand in brands:

            grid.row(
                row_id=brand.pk,
                code=brand.code,
                name=brand.name,
                company=brand.company.name,
                is_active=brand.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:brand-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:brand-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="assets:brand-delete",
        )

        grid.paginate(brands)

        return PageDTO(
            title="Brands",
            subtitle="Manage Brands",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Brands",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New Brand",
                        icon="bi-plus-lg",
                        url=reverse(
                            "assets:brand-create",
                        ),
                        style="warning",
                    ),
                ],
            ),
            content=grid.build(),
        )
    # =====================================================
    # Create Page
    # =====================================================

    def create_page(self):

        form = BrandCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Brand",
                form=form,
            )

            .section("Brand Information")

            .field("company", width=6)
            

            .field("name", width=8)
            

            .field("description", width=12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "assets:brand-list",
            )

            .build()
        )

        return PageDTO(
            title="Create Brand",
            subtitle="Create a new brand",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Brands",
                    url=reverse(
                        "assets:brand-list",
                    ),
                ),
                BreadcrumbDTO(
                    label="Create",
                ),
            ],
            content=form_dto,
        )



    # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        brand,
    ):

        form = BrandUpdateForm(
            instance=brand,
        )

        # Make every field read-only
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Brand Details",
                form=form,
            )

            .section("Brand Information")

            .field("company", width=6)
            
            .field("name", width=8)
           
            .field("description", width=12)

            .field("is_active", width=12)

            .reverse(
                "assets:brand-list",
            )

            .build()
        )

        return PageDTO(
            title="Brand Details",
            subtitle=brand.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Brands",
                    url=reverse(
                        "assets:brand-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=brand.name,
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:brand-update",
                            kwargs={"pk": brand.pk},
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:brand-list",
                        ),
                        style="secondary",
                    ),
                ],
            ),
            content=form_dto,
        )

    # =====================================================
    # Update Page
    # =====================================================

    def update_page(
        self,
        brand,
    ):

        form = BrandUpdateForm(
            instance=brand,
        )

        form_dto = (
            FormBuilder(
                title="Edit Brand",
                form=form,
            )

            .section("Brand Information")

            .field("company", width=6)
            

            .field("name", width=8)
          

            .field("description", width=12)

            .section("System")

            .field("is_active", width=12)

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "assets:brand-list",
            )

            .build()
        )

        return PageDTO(
            title="Edit Brand",
            subtitle=brand.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Brands",
                    url=reverse(
                        "assets:brand-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=brand.name,
                    url=reverse(
                        "assets:brand-detail",
                        args=[brand.pk],
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],
            content=form_dto,
        )