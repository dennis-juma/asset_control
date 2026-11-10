from accounts.models.choices import UserType


ROLE_PERMISSIONS = {
    UserType.SUPER_ADMIN: "__ALL__",

    UserType.ADMIN: [
        # Asset document processing
        "document_processing.view_extractionbatch",
        "document_processing.process_documents",
        "document_processing.review_extracted_records",
        "document_processing.export_extracted_records",
        # Assets
        "assets.view_asset",
        "assets.add_asset",
        "assets.change_asset",
        "assets.delete_asset",
        "assets.assign_asset",
        "assets.transfer_asset",
        "assets.export_asset",

        # Employees
        "employees.view_employee",
        "employees.add_employee",
        "employees.change_employee",

        # Organizations
        "organizations.view_country",
        "organizations.view_site",
        "organizations.view_department",
        "organizations.view_jobtitle",
        "organizations.view_region",
        "organizations.view_currency",

        "organizations.add_country",
        "organizations.add_site",
        "organizations.add_department",
        "organizations.add_jobtitle",
        "organizations.add_region",
        "organizations.add_currency",

        "organizations.change_country",
        "organizations.change_site",
        "organizations.change_department",
        "organizations.change_jobtitle",
        "organizations.change_region",
        "organizations.change_currency",

        # Maintenance
        "maintenance.view_maintenance",
        "maintenance.add_maintenance",
        "maintenance.change_maintenance",
    ],

    UserType.COUNTRY_ADMIN: [
        # Asset document processing
        "document_processing.view_extractionbatch",
        "document_processing.process_documents",
        "document_processing.review_extracted_records",
        "document_processing.export_extracted_records",
        # Assets
        "assets.view_asset",
        "assets.add_asset",
        "assets.change_asset",
        "assets.assign_asset",
        "assets.transfer_asset",
        "assets.export_asset",

        # Employees
        "employees.view_employee",
        "employees.add_employee",
        "employees.change_employee",

        # Organizations - read only
        "organizations.view_country",
        "organizations.view_site",
        "organizations.view_department",
        "organizations.view_jobtitle",
        "organizations.view_region",
        "organizations.view_currency",

        # Maintenance
        "maintenance.view_maintenance",
        "maintenance.add_maintenance",
        "maintenance.change_maintenance",
    ],

    UserType.USER: [
        "assets.view_asset",
        "employees.view_employee",
        "maintenance.view_maintenance",
    ],
}
