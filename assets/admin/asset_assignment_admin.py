from django.contrib import admin, messages
from django.shortcuts import redirect


from api import urls
from assets.choices.choices import AssignmentStatus
from assets.models import AssetAssignment
from django.urls import path, reverse
from assets.views.transfer import AssetTransferView


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        #"asset",
        "employee",
        "status_badge",
        "assigned_date",
        "expected_return_date",
        "returned_date",
        "assigned_by",
    )

    list_display_links = (
        #"asset",
        "employee",
    )

    search_fields = (
        "asset__asset_tag",
        "asset__serial_number",
        "employee__employee_id",
        "employee__first_name",
        "employee__last_name",
        "employee__work_email",
    )

    list_filter = (
        "status",
        "assigned_date",
        "assigned_by",
    )

    list_select_related = (
        #"asset",
        "employee",
        "assigned_by",
        "returned_by",
    )

    autocomplete_fields = (
        #"asset",
        "employee",
        "assigned_by",
        "returned_by",
    )

    readonly_fields = (
        "id",
        "slug",
        "assigned_date",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-assigned_date",
    )

    date_hierarchy = "assigned_date"

    list_per_page = 25

    actions = [
        "return_assets",
        "transfer_asset",

    ]

    fieldsets = (
        (
            "Assignment Information",
            {
                "fields": (
                    #"asset",
                    "employee",
                    "assigned_by",
                    "assigned_date",
                ),
            },
        ),
        (
            "Return Information",
            {
                "fields": (
                    "expected_return_date",
                    "returned_by",
                    "returned_date",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "notes",
                ),
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

    @admin.display(description="Status")
    def status_badge(self, obj):
        if obj.status == AssignmentStatus.ACTIVE:
            return "🟢 Active"
        return "⚪ Returned"

    @admin.action(description="Return selected assets")
    def return_assets(self, request, queryset):
        updated = 0

        for assignment in queryset:
            if assignment.status == AssignmentStatus.ACTIVE:
                assignment.mark_returned(request.user)
                updated += 1

        self.message_user(
            request,
            f"{updated} asset(s) returned successfully.",
        )

    def save_model(self, request, obj, form, change):
        """
        Automatically record who assigned the asset.
        """
        if not change:
            obj.assigned_by = request.user

        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """
        Once an assignment exists, assignment details cannot be changed.
        Returned assignments become completely read-only.
        """
        readonly = list(self.readonly_fields)

        if obj:
            readonly.extend(
                [
                    "assigned_by",
                    "assigned_date",
                ]
            )

        if obj and obj.status == AssignmentStatus.RETURNED:
            return [field.name for field in obj._meta.fields]

        return readonly

    def has_delete_permission(self, request, obj=None):
        return False


    @admin.action(description="Transfer selected asset")
    def transfer_asset(modeladmin, request, queryset):
        if queryset.count() != 1:
            messages.error(
                request,
                "Please select exactly one active assignment."
            )
            return

        assignment = queryset.first()

        url = reverse(
            "admin:asset-transfer",
            args=[assignment.pk],
        )

        return redirect(url)
    


    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:pk>/transfer/",
                self.admin_site.admin_view(
                    AssetTransferView.as_view()
                ),
                name="asset-transfer",
            ),
        ]

        return custom_urls + urls