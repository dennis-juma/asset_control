from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from core.services.country_context import CountryContextService


class CountrySwitchView(LoginRequiredMixin, View):

    def get(self, request):

        country_id = request.GET.get("country")

        if country_id == "all":
            if request.user.user_type == "SUPER_ADMIN":
                CountryContextService.set_global_session(
                    request,
                )

                messages.success(
                    request,
                    "Country context changed to All Countries.",
                )

            else:
                messages.error(
                    request,
                    "You do not have access to all countries.",
                )

            return self._redirect_back(request)

        if not country_id:
            CountryContextService.clear_session_country(
                request,
            )

            return self._redirect_back(request)

        context = CountryContextService.resolve(
            request.user,
            country_id,
        )

        if not context.country:
            messages.error(
                request,
                "You do not have access to the selected country.",
            )

            return self._redirect_back(request)

        CountryContextService.set_session_country(
            request,
            context.country.pk,
        )

        messages.success(
            request,
            f"Country changed to {context.country.name}.",
        )

        return self._redirect_back(request)

    @staticmethod
    def _redirect_back(request):

        return redirect(
            request.META.get(
                "HTTP_REFERER",
                "/",
            )
        )