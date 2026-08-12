from django.urls import reverse

from assets.forms import (
    AssetAttachmentCreateForm,
    AssetAttachmentUpdateForm,
)

from assets.repositories.asset_attachment_repository import (
    AssetAttachmentRepository,
)

from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)

from core.dtos.toolbar import (
    Toolbar,
    ToolbarButton,
)

from core.ui.forms.builder import FormBuilder


class AssetAttachmentPageService:

    def __init__(self):
        self.repository = AssetAttachmentRepository()

    # =====================================================
    # Create Page
    # =====================================================

    def create_page(
        self,
        asset,
        form=None,
    ):

        if form is None:
            form = AssetAttachmentCreateForm(
                asset=asset,
            )

        form_dto = (
            FormBuilder(
                title="Add Attachment",
                form=form,
                 action=(
                     reverse(
                "assets:asset-attachment-create",
            )
            + f"?asset={asset.pk}"
                 )

            )

            .section("Attachment Information")

            .field(
                "attachment_type",
                width=6,
            )

            .field(
                "file",
                width=6,
            )

            .field(
                "description",
                width=12,
            )

            .submit(
                "Upload Attachment",
                icon="cloud-upload",
            )

            .reverse(
                "assets:asset-detail",
                kwargs={
                    "pk": asset.pk,
                },
            )

            .build()
        )

        return PageDTO(
            title="Add Attachment",
            subtitle=asset.asset_tag,

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={
                            "pk": asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="Add Attachment",
                ),
            ],

            content=form_dto,
        )

    # =====================================================
    # Detail Page
    # =====================================================

    def detail_page(
        self,
        attachment,
    ):

        form = AssetAttachmentUpdateForm(
            instance=attachment,
        )

        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(
                title="Attachment Details",
                form=form,
            )

            .section("Attachment Information")

            .field(
                "attachment_type",
                width=6,
            )

            .field(
                "description",
                width=12,
            )

            .reverse(
                "assets:asset-detail",
                kwargs={
                    "pk": attachment.asset.pk,
                },
            )

            .build()
        )

        return PageDTO(
            title="Attachment Details",
            subtitle=attachment.asset.asset_tag,

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=attachment.asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={
                            "pk": attachment.asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="Attachment",
                ),
            ],

            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "assets:asset-attachment-update",
                            kwargs={
                                "pk": attachment.pk,
                            },
                        ),
                        style="primary",
                    ),

                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse(
                            "assets:asset-detail",
                            kwargs={
                                "pk": attachment.asset.pk,
                            },
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
        attachment,
        form=None,
    ):

        if form is None:
            form = AssetAttachmentUpdateForm(
                instance=attachment,
            )

        form_dto = (
            FormBuilder(
                title="Edit Attachment",
                form=form,
            )

            .section("Attachment Information")

            .field(
                "attachment_type",
                width=6,
            )

            .field(
                "description",
                width=12,
            )

            .submit(
                "Update Attachment",
                icon="save",
            )

            .reverse(
                "assets:asset-attachment-detail",
                kwargs={
                    "pk": attachment.pk,
                },
            )

            .build()
        )

        return PageDTO(
            title="Edit Attachment",
            subtitle=attachment.asset.asset_tag,

            breadcrumb=[
                BreadcrumbDTO(
                    label="Assets",
                    url=reverse(
                        "assets:asset-list",
                    ),
                ),

                BreadcrumbDTO(
                    label=attachment.asset.asset_tag,
                    url=reverse(
                        "assets:asset-detail",
                        kwargs={
                            "pk": attachment.asset.pk,
                        },
                    ),
                ),

                BreadcrumbDTO(
                    label="Edit Attachment",
                ),
            ],

            content=form_dto,
        )