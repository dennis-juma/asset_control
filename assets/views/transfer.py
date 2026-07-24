from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from assets.forms.transfer import AssetTransferForm
from assets.models import AssetAssignment
from assets.services.transfer_service import AssetTransferService


class AssetTransferView(View):
    template_name = "admin/assets/transfer.html"

    def get(self, request, pk):
        assignment = get_object_or_404(
            AssetAssignment,
            pk=pk,
        )

        form = AssetTransferForm()

        return render(
            request,
            self.template_name,
            {
                "assignment": assignment,
                "form": form,
            },
        )

    def post(self, request, pk):
        assignment = get_object_or_404(
            AssetAssignment,
            pk=pk,
        )

        form = AssetTransferForm(request.POST)

        if form.is_valid():
            AssetTransferService.transfer(
                assignment=assignment,
                employee=form.cleaned_data["employee"],
                assigned_by=request.user,
                assigned_date=form.cleaned_data["assigned_date"],
                expected_return_date=form.cleaned_data["expected_return_date"],
                notes=form.cleaned_data["notes"],
            )

            messages.success(
                request,
                "Asset transferred successfully."
            )

            return redirect(
                "admin:assets_assetassignment_changelist"
            )

        return render(
            request,
            self.template_name,
            {
                "assignment": assignment,
                "form": form,
            },
        )