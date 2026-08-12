from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from core.permissions.constants import Permissions
from core.permissions.mixins import PermissionRequiredMixin

from assets.dtos.asset_attachment import (
    AssetAttachmentCreateDTO,
    AssetAttachmentUpdateDTO,
)

from assets.forms.asset_attachment import (
    AssetAttachmentCreateForm,
    AssetAttachmentUpdateForm,
)

from assets.models import Asset

from assets.page_services.asset_attachment_page_service import (
    AssetAttachmentPageService,
)

from assets.repositories.asset_attachment_repository import (
    AssetAttachmentRepository,
)

from assets.services.asset_attachment_service import (
    AssetAttachmentService,
)


class AssetAttachmentCreateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get_asset(self, request):

        asset_id = request.GET.get("asset")

        if not asset_id:
            return None

        return get_object_or_404(Asset, pk=asset_id)

    def get(self, request, *args, **kwargs):

        asset = self.get_asset(request)

        if asset is None:
            messages.error(
                request,
                "Please select an asset before adding an attachment.",
            )

            return redirect(
                "assets:asset-list",
            )

        page = AssetAttachmentPageService().create_page(
            asset=asset,
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request, *args, **kwargs):

        asset = self.get_asset(request)

        if asset is None:
            messages.error(
                request,
                "Please select an asset before adding an attachment.",
            )

            return redirect(
                "assets:asset-list",
            )

        form = AssetAttachmentCreateForm(
            request.POST,
            request.FILES,
            asset=asset,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page":
                    AssetAttachmentPageService().create_page(
                        asset=asset,
                        form=form,
                    ),
                }
            )

        dto = AssetAttachmentCreateDTO(
            asset=asset,
            attachment_type=form.cleaned_data[
                "attachment_type"
            ],
            file=form.cleaned_data[
                "file"
            ],
            description=form.cleaned_data[
                "description"
            ],
        )

        try:

            attachment = (
                AssetAttachmentService().create(
                    dto,
                    performed_by=(
                        request.user
                        if request.user.is_authenticated
                        else None
                    ),
                )
            )

        except ValidationError as exc:

            if hasattr(exc, "message_dict"):

                for field, errors in (
                    exc.message_dict.items()
                ):

                    for error in errors:

                        form.add_error(
                            field,
                            error,
                        )

            else:

                form.add_error(
                    None,
                    str(exc),
                )

            return self.render_to_response(
                {
                    "page":
                    AssetAttachmentPageService().create_page(
                        asset=asset,
                        form=form,
                    ),
                }
            )

        messages.success(
            request,
            "Attachment uploaded successfully.",
        )

        return redirect(
            "assets:asset-attachment-detail",
            pk=attachment.pk,
        )


class AssetAttachmentDetailView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_VIEW

    template_name = "crud/form.html"

    def get(self, request, pk, *args, **kwargs):

        attachment = (
            AssetAttachmentRepository().get(pk)
        )

        page = (
            AssetAttachmentPageService()
            .detail_page(
                attachment,
            )
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetAttachmentUpdateView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    template_name = "crud/form.html"

    def get(self, request, pk, *args, **kwargs):

        attachment = (
            AssetAttachmentRepository().get(pk)
        )

        page = (
            AssetAttachmentPageService()
            .update_page(
                attachment,
            )
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )

    def post(self, request, pk, *args, **kwargs):

        attachment = (
            AssetAttachmentRepository().get(pk)
        )

        form = AssetAttachmentUpdateForm(
            request.POST,
            instance=attachment,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page":
                    AssetAttachmentPageService()
                    .update_page(
                        attachment,
                        form,
                    ),
                }
            )

        dto = AssetAttachmentUpdateDTO(
            attachment_type=form.cleaned_data[
                "attachment_type"
            ],
            description=form.cleaned_data[
                "description"
            ],
        )

        try:

            AssetAttachmentService().update(
                attachment,
                dto,
                performed_by=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),
            )

        except ValidationError as exc:

            if hasattr(exc, "message_dict"):

                for field, errors in (
                    exc.message_dict.items()
                ):

                    for error in errors:

                        form.add_error(
                            field,
                            error,
                        )

            else:

                form.add_error(
                    None,
                    str(exc),
                )

            return self.render_to_response(
                {
                    "page":
                    AssetAttachmentPageService()
                    .update_page(
                        attachment,
                        form,
                    ),
                }
            )

        messages.success(
            request,
            "Attachment updated successfully.",
        )

        return redirect(
            "assets:asset-attachment-detail",
            pk=attachment.pk,
        )


class AssetAttachmentDeleteView(
    PermissionRequiredMixin,
    TemplateView):
    permission_required = Permissions.ASSET_UPDATE

    def post(self, request, pk, *args, **kwargs):

        attachment = (
            AssetAttachmentRepository().get(pk)
        )

        asset_pk = attachment.asset.pk

        try:

            AssetAttachmentService().delete(
                attachment,
                performed_by=(
                    request.user
                    if request.user.is_authenticated
                    else None
                ),
            )

        except ValidationError as exc:

            messages.error(
                request,
                str(exc),
            )

            return redirect(
                "assets:asset-attachment-detail",
                pk=pk,
            )

        messages.success(
            request,
            "Attachment deleted successfully.",
        )

        return redirect(
            "assets:asset-detail",
            pk=asset_pk,
        )
