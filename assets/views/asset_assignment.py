from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from assets.dtos import (
    AssetAssignmentCreateDTO,
    AssetAssignmentUpdateDTO,
    AssetReturnDTO,
)
from assets.forms import (
    AssetAssignmentCreateForm,
    AssetAssignmentUpdateForm,
    AssetReturnForm,
)
from assets.page_services import AssetAssignmentPageService
from assets.repositories import AssetAssignmentRepository
from assets.services import AssetAssignmentService


class AssetAssignmentListView(TemplateView):

    template_name = "crud/list.html"

    def get(self, request, *args, **kwargs):

        page = AssetAssignmentPageService().list_page(
            query=request.GET.get("q", ""),
            page=request.GET.get("page", 1),
        )

        return self.render_to_response(
            {
                "page": page,
            }
        )


class AssetAssignmentCreateView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request):

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().create_page(),
            }
        )

    def post(self, request):

        form = AssetAssignmentCreateForm(request.POST)

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().create_page(
                        form,
                    ),
                }
            )

        dto = AssetAssignmentCreateDTO(
        
            company=form.cleaned_data["company"],
            asset=form.cleaned_data["asset"],
            assignment_type=form.cleaned_data["assignment_type"],
            employee=form.cleaned_data["employee"],
            site=form.cleaned_data["site"],
            assigned_date=form.cleaned_data["assigned_date"],
            expected_return_date=form.cleaned_data["expected_return_date"],
            remarks=form.cleaned_data["remarks"],
        )

        AssetAssignmentService().create(dto)

        messages.success(
            request,
            "Asset assigned successfully.",
        )

        return redirect(
            "assets:asset-assignment-list",
        )


class AssetAssignmentDetailView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().detail_page(
                    assignment,
                ),
            }
        )


class AssetAssignmentUpdateView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().update_page(
                    assignment,
                ),
            }
        )

    def post(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        form = AssetAssignmentUpdateForm(
            request.POST,
            instance=assignment,
        )

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().update_page(
                        assignment,
                        form,
                    ),
                }
            )

        dto = AssetAssignmentUpdateDTO(
            employee=form.cleaned_data["employee"],
            site=form.cleaned_data["site"],
            assigned_date=form.cleaned_data["assigned_date"],
            expected_return_date=form.cleaned_data["expected_return_date"],
            remarks=form.cleaned_data["remarks"],
            is_active=form.cleaned_data["is_active"],
        )

        AssetAssignmentService().update(
            assignment,
            dto,
        )

        messages.success(
            request,
            "Assignment updated successfully.",
        )

        return redirect(
            "assets:asset-assignment-list",
        )


class AssetReturnView(TemplateView):

    template_name = "crud/form.html"

    def get(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        return self.render_to_response(
            {
                "page": AssetAssignmentPageService().return_page(
                    assignment,
                ),
            }
        )

    def post(self, request, pk):

        assignment = AssetAssignmentRepository().get(pk)

        form = AssetReturnForm(request.POST)

        if not form.is_valid():

            return self.render_to_response(
                {
                    "page": AssetAssignmentPageService().return_page(
                        assignment,
                        form,
                    ),
                }
            )

        dto = AssetReturnDTO(
            returned_date=form.cleaned_data["returned_date"],
            remarks=form.cleaned_data["remarks"],
        )

        AssetAssignmentService().return_asset(
            assignment,
            dto,
        )

        messages.success(
            request,
            "Asset returned successfully.",
        )

        return redirect(
            "assets:asset-assignment-detail",
            pk=assignment.pk,
        )