from django.urls import reverse


from assets.forms import (
    AssetModelCreateForm,
    AssetModelUpdateForm,
)
from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)
from assets.repositories import AssetModelRepository
from core.dtos.toolbar import Toolbar, ToolbarButton
from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder


class AssetModelPageService:

    def __init__(self):
        self.repository = AssetModelRepository()

    # =====================================================
    # List Page
    # =====================================================

    def list_page(
        self,
        query="",
        page=1,
        country_context=None,
    ) -> PageDTO:

        asset_models = self.repository.list(
            query=query,
            page=page,
            country_context=country_context,
        )

        grid = DataGridBuilder("Asset Models")
        grid.search(
    url=reverse("assets:asset-model-list"),
    query=query,
    placeholder="Search asset models...",
)
        grid.bulk_update("assets:asset-model-bulk-update", "models")

        grid.column(
            field="code",
            label="Code",
        )

        grid.column(
            field="name",
            label="Name",
        )


        grid.column(
            field="country",
            label="Country",
        )


        grid.column(
            field="is_active",
            label="Status",
        )

        for asset_model in asset_models:

            grid.row(
                row_id=asset_model.pk,
                code=asset_model.code,
                category=asset_model.category.name,
                brand=asset_model.brand.name,
                name=asset_model.name,
                country=asset_model.country.name,
                is_active=asset_model.is_active,
            )

        grid.action(
            title="View",
            icon="bi-eye",
            url_name="assets:asset-model-detail",
        )

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="assets:asset-model-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="assets:asset-model-delete",
        )

        grid.paginate(asset_models)

        return PageDTO(
            title="Asset Models",
            subtitle="Manage Asset Models",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Models",
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="New Asset Model",
                        icon="bi-plus-lg",
                        url=reverse(
                            "assets:asset-model-create",
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

    def create_page(
            self,
    form=None,
    ):
        if form is None:
            form = AssetModelCreateForm()

        form_dto = (
            FormBuilder(
                title="Create Asset Model",
                form=form,
            )

            .section("Asset Model Information")

            .field("country", width=6)

            .field("category", width=6)

            .field("brand", width=6)

            .field("name", width=6)

            .field("manufacturer_part_number", width=6)

            .field("technical_specifications", width=12)

            .field("description", width=12)

            .submit(
                "Save",
                icon="save",
            )

            .reverse(
                "assets:asset-model-list",
            )

            .build()
        )

        return PageDTO(
            title="Create Asset Model",
            subtitle="Create a new asset model",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Models",
                    url=reverse(
                        "assets:asset-model-list",
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
        asset_model,
    ):

        form = AssetModelUpdateForm(
            instance=asset_model,
        )

        # Make every field read-only
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Asset Model Details",
                form=form,
            )

            .section("Asset Model Information")

            .field("country", width=6)

            .field("category", width=6)

            .field("brand", width=6)

            .field("name", width=6)

            .field("manufacturer_part_number", width=6)

            .field("technical_specifications", width=12)

            .field("description", width=12)

            .field("is_active", width=12)

            .reverse(
                "assets:asset-model-list",
            )

            .build()
        )

        return PageDTO(
            title="Asset Model Details",
            subtitle=asset_model.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Models",
                    url=reverse(
                        "assets:asset-model-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=asset_model.name,
                ),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:asset-model-update",
                            kwargs={"pk": asset_model.pk},
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:asset-model-list",
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
        asset_model,
    ):

        form = AssetModelUpdateForm(
            instance=asset_model,
        )

        form_dto = (
            FormBuilder(
                title="Edit Asset Model",
                form=form,
            )

            .section("Asset Model Information")

            .field("country", width=6)

            .field("category", width=6)

            .field("brand", width=6)

            .field("name", width=6)

            .field("manufacturer_part_number", width=6)

            .field("technical_specifications", width=12)

            .field("description", width=12)

            .field("is_active", width=12)

            .submit(
                "Update",
                icon="save",
            )

            .reverse(
                "assets:asset-model-list",
            )

            .build()
        )

        return PageDTO(
            title="Edit Asset Model",
            subtitle=asset_model.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Asset Models",
                    url=reverse(
                        "assets:asset-model-list",
                    ),
                ),
                BreadcrumbDTO(
                    label=asset_model.name,
                    url=reverse(
                        "assets:asset-model-detail",
                        args=[asset_model.pk],
                    ),
                ),
                BreadcrumbDTO(
                    label="Edit",
                ),
            ],
            content=form_dto,
        )
