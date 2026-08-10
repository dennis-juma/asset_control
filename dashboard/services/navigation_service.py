from django.urls import reverse

from .navigation_item import NavigationItem


class NavigationService:

    def __init__(self, request):
        self.request = request

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
                    ),
                    
                    NavigationItem(
                        title="Categories",
                        icon="bi-diagram-3",
                        url=reverse("assets:asset-category-list"),
                    ),
                    NavigationItem(
                        title="Brands",
                        url=reverse("assets:brand-list"),
                        icon="bi-tags",
                        ),

                    NavigationItem(
                        title="Models",
                        icon="bi bi-pc-display",
                        url=reverse("assets:asset-model-list"),
                    ),
                    NavigationItem(
                        title="Asset",
                        url=reverse("assets:asset-list"),
                        icon="bi-pc-display"
                    ),
                    
                    
                    NavigationItem(
                        title= "Assignments",
                        icon= "bi-person-check",
                        url= reverse(
                            "assets:asset-assignment-list",
                    )),
                    NavigationItem(
                        title="Transfers",
                        icon="bi-arrow-left-right",
                        url=reverse("assets:asset-transfer-list"),
                    ),

                    NavigationItem(
                        title="Vendors",
                        url="#",
                    ),
                ],
            ),

            NavigationItem(
                title="Employees",
                icon="bi-people",
                url=reverse("employees:employee-list"),
            ),

            NavigationItem(
    title="Organizations",
    icon="bi-buildings",
    children=[
        NavigationItem(
            title="Companies",
            url=reverse("organizations:company-list"),
        ),

        NavigationItem(
            title="Countries",
            url=reverse("organizations:country-list"),
        ),

        NavigationItem(
            title="Sites",
            url=reverse("organizations:site-list"),
        ),

        NavigationItem(
            title="Departments",
            url=reverse("organizations:department-list"),
        ),

        NavigationItem(
            title="Job Titles",
            url=reverse("organizations:job-title-list"),
        ),
    ],
),


            NavigationItem(
                title="Assignments",
                icon="bi-arrow-left-right",
                url="#",
            ),

            NavigationItem(
                title="Maintenance",
                icon="bi-tools",
                url="#",
            ),

            NavigationItem(
                title="Reports",
                icon="bi-bar-chart",
                url="#",
            ),

            NavigationItem(
                title="Administration",
                icon="bi-gear",
                url="#",
            ),

            NavigationItem(
                title="Settings",
                icon="bi-sliders",
                url="#",
            ),
        ]

        for item in items:

            if item.url == current_path:
                item.active = True

            for child in item.children:

                if child.url == current_path:
                    child.active = True
                    item.expanded = True

        return items
