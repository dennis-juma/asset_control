from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages

from maintenance.models import Maintenance
from maintenance.choices import MaintenanceStatus
from django.core.exceptions import ValidationError

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
        list_display = (
        "reference",
        "asset",
        "maintenance_type",
        "vendor",
        "status_badge",
        "priority_badge",
        "scheduled_date",
        "estimated_completion_date",
        "completed_date",
        "cost",
        "company",
        "is_active",
    )
        
        search_fields = (
        "reference",
        "asset__asset_tag",
        "asset__serial_number",
        "vendor__name",
        "maintenance_type__name",
        "technician",
        "description",
    )
        actions = (
        "start_maintenance",
        "complete_maintenance",
        "cancel_maintenance",
    )
        
        list_filter = (
        "status",
        "priority",
        "maintenance_type",
        "vendor",
        "company",
        "under_warranty",
        "scheduled_date",
        "completed_date",
        "is_active",
    )
        
        ordering = (
        "-scheduled_date",
        "-created_at",
    )
    
        readonly_fields = (
        "reference",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
        
        autocomplete_fields = (
        "company",
        "asset",
        "maintenance_type",
        "vendor",
        "currency",
    )
        fieldsets = (
        (
            "Maintenance Information",
            {
                "fields": (
                    "reference",
                    "company",
                    "asset",
                    "maintenance_type",
                    "vendor",
                )
            },
        ),
        (
            "Workflow",
            {
                "fields": (
                    "status",
                    "priority",
                )
            },
        ),
        (
            "Scheduling",
            {
                "fields": (
                    "scheduled_date",
                    "started_date",
                    "estimated_completion_date",
                    "completed_date",
                    "next_maintenance_date",
                )
            },
        ),
        (
            "Financial",
            {
                "fields": (
                    "cost",
                    "currency",
                )
            },
        ),
        (
            "Warranty",
            {
                "fields": (
                    "under_warranty",
                    "warranty_claim_number",
                )
            },
        ),
        (
            "Work Details",
            {
                "fields": (
                    "technician",
                    "description",
                    "resolution",
                )
            },
        ),
        (
            "Audit",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                ),
            },
        ),
    )
        
        date_hierarchy = "scheduled_date"
        list_per_page = 25

        @admin.display(description="Status")
        def status_badge(self, obj):
            colors = {
            "SCHEDULED": "#6c757d",
            "IN_PROGRESS": "#0d6efd",
            "COMPLETED": "#198754",
            "CANCELLED": "#dc3545",
        }

            color = colors.get(obj.status, "#6c757d")

            return format_html(
            '<span style="background:{};color:white;'
            'padding:4px 8px;border-radius:10px;">{}</span>',
            color,
            obj.get_status_display(),
        )

        @admin.display(description="Priority")
        def priority_badge(self, obj):
            colors = {
                "LOW": "#198754",
                "MEDIUM": "#ffc107",
                "HIGH": "#fd7e14",
                "CRITICAL": "#dc3545",
            }

            color = colors.get(obj.priority, "#6c757d")

            return format_html(
                '<strong style="color:{};">{}</strong>',
                color,
                obj.get_priority_display(),
            )
        
        from django.contrib import messages


        @admin.action(description="Start selected maintenance")
        def start_maintenance(self, request, queryset):
            success = 0

            for maintenance in queryset:
                try:
                    maintenance.start()
                    success += 1
                except ValidationError as e:
                    self.message_user(
                        request,
                        f"{maintenance.reference}: {e}",
                        level=messages.ERROR,
                    )

            if success:
                self.message_user(
                    request,
                    f"{success} maintenance record(s) started.",
                    level=messages.SUCCESS,
                )
        


        @admin.action(description="Complete selected maintenance")
        def complete_maintenance(self, request, queryset):
            success = 0

            for maintenance in queryset:
                try:
                    maintenance.complete()
                    success += 1
                except ValidationError as e:
                    self.message_user(
                        request,
                        f"{maintenance.reference}: {e}",
                        level=messages.ERROR,
                    )

            if success:
                self.message_user(
                    request,
                    f"{success} maintenance record(s) completed.",
                    level=messages.SUCCESS,
                )

        @admin.action(description="Cancel selected maintenance")
        def cancel_maintenance(self, request, queryset):
            success = 0

            for maintenance in queryset:
                try:
                    maintenance.cancel()
                    success += 1
                except ValidationError as e:
                    self.message_user(
                        request,
                        f"{maintenance.reference}: {e}",
                        level=messages.ERROR,
                    )

            if success:
                self.message_user(
                    request,
                    f"{success} maintenance record(s) cancelled.",
                    level=messages.SUCCESS,
                )
        

        def get_readonly_fields(self, request, obj=None):
            readonly = list(self.readonly_fields)

            if obj:
                readonly.extend(
                    [
                        "reference",
                        "status",
                        "started_date",
                        "completed_date",
                        "previous_asset_status",
                    ]
                )

            return readonly
        



        def has_delete_permission(self, request, obj=None):
            if obj and obj.status == MaintenanceStatus.COMPLETED:
                return False
            return super().has_delete_permission(request, obj)