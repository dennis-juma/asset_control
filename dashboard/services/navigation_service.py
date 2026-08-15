from django.urls import reverse

from core.permissions.service import PermissionService

from .navigation_item import NavigationItem


class NavigationService:

    def __init__(self, request):
        self.request = request
        self.user = request.user

    def get_navigation(self):

        current_path = self.request.path

        items = [

            NavigationItem(
                title="Dashboard",
                icon="bi-speedometer2",
                url=reverse("dashboard:index"),
            ),

            NavigationItem(
                title="Assets",
                icon="bi-laptop",
                children=[
                    NavigationItem(
                        title="All Assets",
                        url="#",
                        permission="assets.view_asset",
                    ),

                    NavigationItem(
                        title="Categories",
                        icon="bi-diagram-3",
                        url=reverse(
                            "assets:asset-category-list"
                        ),
                        permission="assets.view_assetcategory",
                    ),

                    NavigationItem(
                        title="Brands",
                        icon="bi-tags",
                        url=reverse(
                            "assets:brand-list"
                        ),
                        permission="assets.view_brand",
                    ),

                    NavigationItem(
                        title="Models",
                        icon="bi-pc-display",
                        url=reverse(
                            "assets:asset-model-list"
                        ),
                        permission="assets.view_assetmodel",
                    ),

                    NavigationItem(
                        title="Asset",
                        icon="bi-pc-display",
                        url=reverse(
                            "assets:asset-list"
                        ),
                        permission="assets.view_asset",
                    ),

                    NavigationItem(
                        title="Assignments",
                        icon="bi-person-check",
                        url=reverse(
                            "assets:asset-assignment-list"
                        ),
                        permission="assets.view_assetassignment",
                    ),

                    NavigationItem(
                        title="Transfers",
                        icon="bi-arrow-left-right",
                        url=reverse(
                            "assets:asset-transfer-list"
                        ),
                        permission="assets.view_assettransfer",
                    ),

                    NavigationItem(
                        title="Vendors",
                        url="#",
                        permission="assets.view_vendor",
                    ),
                ],
            ),

            NavigationItem(
                title="Employees",
                icon="bi-people",
                url=reverse(
                    "employees:employee-list"
                ),
                permission="employees.view_employee",
            ),

            NavigationItem(
                title="Organizations",
                icon="bi-buildings",
                children=[
                    NavigationItem(
                        title="Countries",
                        url=reverse(
                            "organizations:country-list"
                        ),
                        permission="organizations.view_country",
                    ),

                    NavigationItem(
                        title="Sites",
                        url=reverse(
                            "organizations:site-list"
                        ),
                        permission="organizations.view_site",
                    ),

                    NavigationItem(
                        title="Departments",
                        url=reverse(
                            "organizations:department-list"
                        ),
                        permission="organizations.view_department",
                    ),

                    NavigationItem(
                        title="Job Titles",
                        url=reverse(
                            "organizations:job-title-list"
                        ),
                        permission="organizations.view_jobtitle",
                    ),
                ],
            ),

            NavigationItem(
                title="Maintenance",
                icon="bi-tools",
                url="#",
                permission="maintenance.view_maintenance",
            ),

            NavigationItem(
                title="Reports",
                icon="bi-bar-chart",
                url="#",
                permission="assets.export_asset",
            ),

            NavigationItem(
                title="Administration",
                icon="bi-gear",
                url="#",
                permission="accounts.view_user",
            ),

            NavigationItem(
                title="Settings",
                icon="bi-sliders",
                url="#",
                permission="organizations.change_company",
            ),
        ]

        items = self._filter_items(items)

        self._set_active_items(
            items,
            current_path,
        )

        return items

    def _filter_items(self, items):

        visible_items = []

        for item in items:

            # Filter children first.
            if item.children:

                visible_children = self._filter_items(
                    item.children
                )

                item.children = visible_children

                # A parent with children is visible
                # only when at least one child is visible.
                if not visible_children:
                    continue

            # If the item requires permission,
            # check it against the current user.
            if item.permission:

                if not PermissionService.can(
                    self.user,
                    item.permission,
                ):
                    continue

            visible_items.append(item)

        return visible_items

    @staticmethod
    def _set_active_items(
        items,
        current_path,
    ):

        for item in items:

            if item.url == current_path:
                item.active = True

            for child in item.children:

                if child.url == current_path:
                    child.active = True
                    item.expanded = True