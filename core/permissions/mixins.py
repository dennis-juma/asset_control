from dataclasses import replace
from urllib.parse import quote

from django.shortcuts import redirect
from django.urls import reverse

from core.permissions.service import PermissionService
from core.ui.actions.permissions import (
    ActionPermissionService,
)


class PermissionRequiredMixin:

    permission_required = None

    def dispatch(
        self,
        request,
        *args,
        **kwargs,
    ):

        if not request.user.is_authenticated:
            login_url = reverse("accounts:login")
            next_url = quote(request.get_full_path())
            return redirect(f"{login_url}?next={next_url}")

        if self.permission_required:
            PermissionService.require(
                request.user,
                self.permission_required,
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def filter_page_permissions(
        self,
        page,
        user,
    ):

        if user.is_superuser:
            return page

        toolbar = page.toolbar

        if toolbar:
            toolbar = toolbar.filter_permissions(
                user
            )

        content = page.content

        if content:

            if hasattr(
                content,
                "filter_permissions",
            ):
                content = content.filter_permissions(
                    user
                )

            elif hasattr(
                content,
                "actions",
            ):
                content = replace(
                    content,
                    actions=ActionPermissionService.filter(
                        content.actions,
                        user,
                    ),
                )

        return replace(
            page,
            toolbar=toolbar,
            content=content,
        )