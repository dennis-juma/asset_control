from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from core.services.country_context import CountryContextService


class BulkStatusUpdateView(View):
    """Apply an active/inactive status to selected, in-scope records."""

    model = None
    redirect_url = None
    record_label = "record"

    def post(self, request, *args, **kwargs):
        selected_ids = list(dict.fromkeys(request.POST.getlist("selected_ids")))
        status = request.POST.get("status")

        if not selected_ids:
            messages.error(request, "Select at least one record.")
            return redirect(self.redirect_url)

        if status not in {"active", "inactive"}:
            messages.error(request, "Choose a valid status.")
            return redirect(self.redirect_url)

        queryset = self.model.objects.filter(pk__in=selected_ids)
        country_context = CountryContextService.resolve_request(request)

        if country_context.country:
            queryset = queryset.filter(country=country_context.country)
        elif request.user.user_type != "SUPER_ADMIN":
            queryset = queryset.none()

        updated = queryset.update(
            is_active=status == "active",
            updated_at=timezone.now(),
        )

        messages.success(
            request,
            f"Updated {updated} {self.record_label}{'' if updated == 1 else 's'}.",
        )

        return redirect(self.redirect_url)
