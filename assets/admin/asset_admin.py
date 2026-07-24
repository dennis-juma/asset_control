from django.contrib import admin

from assets.choices.choices import AssignmentStatus
from assets.models import Asset
from .inlines import AssetAssignmentInline


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_tag",
        "company",
        "category",
        "brand",
        "model",
        "serial_number",
        "status",
        "condition",
        "purchase_date",
        "is_under_warranty",
        "current_holder",
        "is_active",
    )

    list_display_links = (
        "asset_tag",
        "serial_number",
    )

    search_fields = (
        "asset_tag",
        "serial_number",
        "barcode",
        "invoice_number",
        "po_number",
    )

    list_filter = (
        "company",
        "category",
        "brand",
        "model",
        "vendor",
        "status",
        "condition",
        "currency",
        "is_active",
    )

    readonly_fields = (
        "id",
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    autocomplete_fields = (
        "company",
        "category",
        "brand",
        "model",
        "vendor",
        "currency",
    )

    fieldsets = (
        (
            "Identification",
            {
                "fields": (
                    "asset_tag",
                    "serial_number",
                    "barcode",
                )
            },
        ),
        (
            "Classification",
            {
                "fields": (
                    "company",
                    "category",
                    "brand",
                    "model",
                    "vendor",
                )
            },
        ),
        (
            "Purchase Information",
            {
                "fields": (
                    "purchase_date",
                    "purchase_price",
                    "currency",
                    "invoice_number",
                    "po_number",
                )
            },
        ),
        (
            "Warranty",
            {
                "fields": (
                    "warranty_start",
                    "warranty_end",
                    "is_under_warranty",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "condition",
                    "is_active",
                )
            },
        ),
        (
            "System Information",
            {
                "classes": ("collapse",),
                "fields": (
                    "id",
                    "slug",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
    inlines = [
    AssetAssignmentInline,
]
    
    @admin.display(description="Current Holder")
    def current_holder(self, obj):
        assignment = (
        obj.assignments.filter(
            status=AssignmentStatus.ACTIVE
        )
        .select_related("employee")
        .first()
    )

        if assignment:
          
            return str(assignment.employee)
        

        return "-"

    @admin.display(boolean=True, description="Under Warranty")
    def warranty_status(self, obj):
        return obj.is_under_warranty