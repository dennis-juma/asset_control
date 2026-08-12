from django.urls import reverse

from core.dtos import (
    BreadcrumbDTO,
    PageDTO,
)


from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder
from core.dtos.toolbar import Toolbar, ToolbarButton


from organizations.forms import (
    SiteCreateForm,
    SiteUpdateForm,
)

from organizations.repositories import SiteRepository
from organizations.services import SiteService


class SitePageService:

    def __init__(self):

        self.service = SiteService()

        self.repository = SiteRepository()

    def list_page(
    self,
    query="",
    page=1,
) -> PageDTO:
        sites = self.repository.list(
    query=query,
    page=page,
)
        grid = DataGridBuilder("Sites")
        grid.column(
    field="code",
    label="Code",
)

        grid.column(
            field="name",
            label="Site",
        )

        grid.column(
            field="country",
            label="Country",
        )

        grid.column(
            field="country",
            label="Country",
        )

        grid.column(
            field="site_type",
            label="Type",
        )

        grid.column(
            field="city",
            label="City",
        )

        grid.column(
            field="is_active",
            label="Status",
        )
        for site in sites:

            grid.row(

                row_id=site.id,

                code=site.code,

                name=site.name,

                country=site.country.name,

                site_type=site.get_site_type_display(),

                city=site.city,

                is_active=site.is_active,

            )
        grid.action(
    title="View",
    icon="bi-eye",
    url_name="organizations:site-detail",
)

        grid.action(
            title="Edit",
            icon="bi-pencil",
            url_name="organizations:site-update",
        )

        grid.action(
            title="Delete",
            icon="bi-trash",
            url_name="organizations:site-delete",
        )

        grid.paginate(sites)
        return PageDTO(

    title="Sites",

    subtitle="Manage sites",

    breadcrumb=[

        BreadcrumbDTO(
            label="Organizations",
            url="/organizations/",
        ),

        BreadcrumbDTO(
            label="Sites",
        ),

    ],

    toolbar=Toolbar(
        buttons=[
            ToolbarButton(
                label="New site",
                icon="bi-plus-lg",
                url=reverse("organizations:site-create"),
                style="warning",
            ),
        ],
    ),

    content=grid.build(),

)

    def create_page(self) -> PageDTO:
        form = SiteCreateForm()

        form_dto = (

    FormBuilder(

        title="Create Site",

        form=form,

    )
        .section("General Information")

        .field(
            "country",
            width=6,
        )

        .field(
            "country",
            width=6,
        )

        .field(
            "name",
            width=6,
        )

        .field(
            "site_type",
            width=6,
        )
            .section("Contact Information")

        .field(
            "email",
            width=6,
        )

        .field(
            "phone",
            width=6,
        )

            .section("Location Information")

        .field(
            "address",
            width=12,
        )

        .field(
            "city",
            width=6,
        )

        .field(
            "postal_code",
            width=6,
        )
            .section("Coordinates")

        .field(
            "latitude",
            width=6,
        )

        .field(
            "longitude",
            width=6,
        )
    

        
            .submit(

        "Save",

        icon="save",

    )

    .reverse(

        "organizations:site-list",

    )

    .build()
    
        )
        return PageDTO(
            
                title="Create Site",
            
                subtitle="Register a new site",
            
                breadcrumb=[
            
                    BreadcrumbDTO(
            
                        label="Organizations",
            
                        url="/organizations/",
            
                    ),
            
                    BreadcrumbDTO(
            
                        label="Sites",
            
                        url=reverse(
                            "organizations:site-list",
                        ),
            
                    ),
            
                    BreadcrumbDTO(
            
                        label="Create",
            
                    ),
            
                ],
            
                content=form_dto,
            
            )



    def detail_page(
    self,
    site,
) -> PageDTO:
        form = SiteUpdateForm(
    instance=site,
)

        for field in form.fields.values():
            field.disabled = True

            form_dto = (
        FormBuilder(
            title="Site Details",
            form=form,
        )
        .section("General Information")
        .field(
            "country",
            width=6,
        )
        .field(
            "country",
            width=6,
        )
        .field(
            "name",
            width=6,
        )
        .field(
            "site_type",
            width=6,
        )
        .section("Contact Information")
        .field(
            "email",
            width=6,
        )
        .field(
            "phone",
            width=6,
        )
        .section("Location Information")
        .field(
            "address",
            width=12,
        )
        .field(
            "city",
            width=6,
        )
        .field(
            "postal_code",
            width=6,
        )
        .section("Coordinates")
        .field(
            "latitude",
            width=6,
        )
        .field(
            "longitude",
            width=6,
        )
        .reverse(
            "organizations:site-list",
        )
        .build()
)
    
        return PageDTO(
            title="Site Details",
            subtitle="View site information",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Sites",
                    url=reverse("organizations:site-list"),
                ),
                BreadcrumbDTO(
                    label=site.name,
                ),
            ],
        toolbar=Toolbar(
    buttons=[
        ToolbarButton(
            label="Edit",
            icon="bi-pencil",
            url=reverse(
                "organizations:site-update",
                kwargs={"pk": site.id},
            ),
            style="warning",
        ),
        ToolbarButton(
            label="Back",
            icon="bi-arrow-left",
            url=reverse("organizations:site-list"),
            style="secondary",
        ),
    ],
),
            content=form_dto,
        )


    def update_page(
    self,
    site,
) -> PageDTO:
        form = SiteUpdateForm(
    instance=site,
)
        form_dto = (

        FormBuilder(

            title="Edit Site",

            form=form,
        )
        .section("General Information")

        .field(
            "country",
            width=6,
        )

        .field(
            "country",
            width=6,
        )

        .field(
            "name",
            width=6,
        )

        .field(
            "site_type",
            width=6,
        )
            .section("Contact Information")

        .field(
            "email",
            width=6,
        )

        .field(
            "phone",
            width=6,
        )

            .section("Location Information")

        .field(
            "address",
            width=12,
        )

        .field(
            "city",
            width=6,
        )

        .field(
            "postal_code",
            width=6,
        )

            .section("Coordinates")

        .field(
            "latitude",
            width=6,
        )

        .field(
            "longitude",
            width=6,
        )

            .section("Additional Information")

            .section("Status")

        .field(
            "is_active",
            width=12,
        )
            .submit(
                "Update",
                icon="save",
            )
            .reverse(
                "organizations:site-list",
            )
            .build()
        )
        return PageDTO(

        title="Edit Site",

        subtitle=site.name,

        breadcrumb=[

            BreadcrumbDTO(
                label="Organizations",
                url="/organizations/",
            ),

            BreadcrumbDTO(
                label="Sites",
                url=reverse(
                    "organizations:site-list",
                ),
            ),

            BreadcrumbDTO(
                label=site.name,
                url=reverse(
                    "organizations:site-detail",
                    args=[site.pk],
                ),
            ),

            BreadcrumbDTO(
                label="Edit",
            ),

        ],

        content=form_dto,

    )
        