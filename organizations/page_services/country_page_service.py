from dataclasses import field

from django.db.models import query
from django.urls import reverse

from core.dtos import BreadcrumbDTO, PageDTO
from core.dtos.toolbar import Toolbar, ToolbarButton
from core.ui.datagrid.builder import DataGridBuilder
from core.ui.forms.builder import FormBuilder

from organizations.forms import CountryCreateForm, CountryUpdateForm
from organizations.repositories import CountryRepository
from organizations.services import CountryService


class CountryPageService:

    def __init__(self):
        self.service = CountryService()
        self.repository = CountryRepository()


    def create_page(self) -> PageDTO:

        form = CountryCreateForm()

        form_dto = (
            FormBuilder(
            
                    title="Create Country",
            
                    form=form,
            
                )

                .section("General Information")
                
                    .field(
                            "name",
                            width=6,
                        )
                        .field(
                            "official_name",
                            width=6,
                        )
                
                        .section("ISO Information")
                        .field(
                            "iso2",
                            width=6,
                        )
                        .field(
                            "iso3",
                            width=6,
                        )
                        .section("Regional Information").field(
                            "phone_code",
                            width=3,
                        )
                        .field(
                            "currency",
                            width=3,
                        )
                        .field(
                            "timezone",
                            width=3,
                        )
                        .field(
                            "continent",
                            width=3,
                        )
                    .section("Additional Information").field(
                            "description",
                            width=12,
                        )
                
                            .submit(
                
                        "Save",
                
                        icon="save",
                
                    )
                
                .cancel(
                    url=reverse("organizations:country-list"),
                    label="Cancel",
                )
                .build()
        )

        return PageDTO(
            title="Create Country",
            subtitle="Register a new country",
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),

                BreadcrumbDTO(
                    label="Countries",  
                    url=reverse(
                        "organizations:country-list",
                    ),
                ),
            ],
            content=form_dto,
        )



    def detail_page(
        self,
        country,
    ) -> PageDTO:

        form = CountryUpdateForm(instance=country)
        for field in form.fields.values():
            field.disabled = True

        form_dto = (
            FormBuilder(title="Country Details", form=form)
            .section("General Information")
            .field("name", width=6)
            .field("official_name", width=6)
            .section("ISO Information")
            .field("iso2", width=6)
            .field("iso3", width=6)
            .section("Regional Information")
            .field("phone_code", width=3)
            .field("currency", width=3)
            .field("timezone", width=3)
            .field("continent", width=3)
            .section("Additional Information")
            .field("description", width=12)
            .reverse("organizations:country-list")
            .build()
        )

        return PageDTO(
            title="Country Details",
            subtitle=country.name,
            breadcrumb=[
                BreadcrumbDTO(label="Organizations", url="/organizations/"),
                BreadcrumbDTO(
                    label="Countries",
                    url=reverse("organizations:country-list"),
                ),
                BreadcrumbDTO(label=country.name),
            ],
            toolbar=Toolbar(
                buttons=[
                    ToolbarButton(
                        label="Edit",
                        icon="bi-pencil",
                        url=reverse(
                            "organizations:country-update",
                            kwargs={"pk": country.id},
                        ),
                        style="warning",
                    ),
                    ToolbarButton(
                        label="Back",
                        icon="bi-arrow-left",
                        url=reverse("organizations:country-list"),
                        style="secondary",
                    ),
                ],
            ),
            content=form_dto,
        )


    def update_page(
        self,
        country,
    ) -> PageDTO:

        form = CountryUpdateForm(
            instance=country,
        )
        form_dto = (
            FormBuilder(
                title="Update Country",
                form=form,
            )
            .section("General Information")
            .field("name", width=6)
            .field("official_name", width=6)
            .section("ISO Information")
            .field("iso2", width=6)
            .field("iso3", width=6)
            .section("Regional Information")
            .field("phone_code", width=3)
            .field("currency", width=3)
            .field("timezone", width=3)
            .field("continent", width=3)
            .section("Additional Information")
            .field("description", width=12)
            .submit(
                "Save",
                icon="save",
            )
            .reverse(
                "organizations:country-list",
            )
            .build()
        )

        return PageDTO(
            title="Update Country",
            subtitle=country.name,
            breadcrumb=[
                BreadcrumbDTO(
                    label="Organizations",
                    url="/organizations/",
                ),
                BreadcrumbDTO(
                    label="Countries",
                    url=reverse("organizations:country-list"),
                ),
                BreadcrumbDTO(
                    label=country.name,
                    url=reverse(
                        "organizations:country-detail",
                        args=[country.id],
                    ),
                ),
                BreadcrumbDTO(
                    label="Update",
                ),
            ],
            content=form_dto,
        )
        
        

    def list_page(
        self,
        query="",
        page=1,
    ) -> PageDTO:

        countries = self.repository.list(
            query=query,
            page=page,
        )

        grid = (

            DataGridBuilder("Countries")

            .column(
                field="code",
                label="Code",
            )

            .column(
                field="name",
                label="Country",
            )

            .column(
                field="iso2",
                label="ISO2",
            )

            .column(
                field="iso3",
                label="ISO3",
            )

            .column(
                field="currency",
                label="Currency",
            )

            .column(
                field="is_active",
                label="Status",
            )

        )

        for country in countries:

            grid.row(

            row_id=country.id,

            code=country.code,

            name=country.name,

            iso2=country.iso2,

            iso3=country.iso3,

            currency=country.currency,

            is_active=country.is_active,

        )

        grid.action(

        title="View",

        icon="bi-eye",

        url_name="organizations:country-detail",

    )

        grid.action(

        title="Edit",

        icon="bi-pencil",

        url_name="organizations:country-update",

    )

        grid.action(

        title="Delete",

        icon="bi-trash",

        url_name="organizations:country-delete",


    )
        grid.paginate(countries)
        return PageDTO(

        title="Countries",

        subtitle="Manage countries",

        breadcrumb=[

            BreadcrumbDTO(

                label="Organizations",

                url="/organizations/",

            ),

            BreadcrumbDTO(

                label="Countries",

            ),

        ],
        toolbar=Toolbar(
                        buttons=[
                            ToolbarButton(
                                label="New country",
                                icon="bi-plus-lg",
                                url=reverse("organizations:country-create"),
                                style="warning",
                            ),
                        ],
                    ),

        content=grid.build(),

    )
