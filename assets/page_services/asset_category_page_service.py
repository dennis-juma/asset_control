from django.urls import reverse

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
    AssetCategoryCreateForm,
    AssetCategoryUpdateForm,
)
from assets.repositories import AssetCategoryRepository


class AssetCategoryPageService:

    def __init__(self):
        self.repository = AssetCategoryRepository()

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
        self,
        query="",
        page=1,
    ) -> PageDTO:

        categories = self.repository.list(
            query=query,
            page=page,
        )

        grid = DataGridBuilder("Asset Categories")

        grid.column(
            field="code",
            label="Code",
        )

        grid.column(
            field="name",
            label="Category",
        )

        grid.column(
            field="parent",
            label="Parent",
        )

        grid.column(
            field="country",
            label="Country",
        )

        grid.column(
            field="sort_order",
            label="Sort Order",
        )

        grid.column(
            field="is_active",
            label="Status",
        )

        for category in categories:

            grid.row(
                row_id=category.pk,
                code=category.code,
                name=category.name,
                parent=category.parent.name if category.parent else "-",
                country=category.country.name,
                sort_order=category.sort_order,
                is_active=category.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:asset-category-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:asset-category-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="assets:asset-category-delete",
        )

        grid.paginate(categories)

        return PageDTO(
            title="Asset Categories",
            subtitle="Manage Asset Categories",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Categories",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New Category",
                        icon="bi-plus-lg",
                        url=reverse(
                            "assets:asset-category-create",
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

        form = AssetCategoryCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Asset Category",
                form=form,
            )

            .section("Category Information")

            .field("country", width=6)
            .field("parent", width=6)

            .field("name", width=8)
            .field("sort_order", width=4)

            .field("description", width=12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "assets:asset-category-list",
            )

            .build()
        )

        return PageDTO(
            title="Create Asset Category",
            subtitle="Create a new asset category",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Categories",
                    url=reverse(
                        "assets:asset-category-list",
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
        category,
    ):

        form = AssetCategoryUpdateForm(
            instance=category,
        )

        # Make every field read-only
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Asset Category Details",
                form=form,
            )

            .section("Category Information")

            .field("country", width=6)
            .field("parent", width=6)

            .field("name", width=8)
            .field("sort_order", width=4)

            .field("description", width=12)

            .field("is_active", width=12)

            .reverse(
                "assets:asset-category-list",
            )

            .build()
        )

        return PageDTO(
            title="Asset Category Details",
            subtitle=category.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Categories",
                    url=reverse(
                        "assets:asset-category-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=category.name,
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:asset-category-update",
                            kwargs={"pk": category.pk},
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:asset-category-list",
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
        category,
    ):

        form = AssetCategoryUpdateForm(
            instance=category,
        )

        form_dto = (
            FormBuilder(
                title="Edit Asset Category",
                form=form,
            )

            .section("Category Information")

            .field("country", width=6)
            .field("parent", width=6)

            .field("name", width=8)
            .field("sort_order", width=4)

            .field("description", width=12)

            .section("System")

            .field("is_active", width=12)

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "assets:asset-category-list",
            )

            .build()
        )

        return PageDTO(
            title="Edit Asset Category",
            subtitle=category.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Categories",
                    url=reverse(
                        "assets:asset-category-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=category.name,
                    url=reverse(
                        "assets:asset-category-detail",
                        args=[category.pk],
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],
            content=form_dto,
        )