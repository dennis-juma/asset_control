from assets.models import AssetAssignment
from assets.choices import AssignmentStatus


class AssetNotificationService:

    @staticmethod
    def employee_assets(employee):
        """
        Return all assets currently actively assigned
        to an employee.
        """

        return (
            AssetAssignment.objects
            .filter(
                employee=employee,
                status=AssignmentStatus.ACTIVE,
            )
            .select_related(
                "asset",
                "asset__asset_model",
                "asset__asset_model__brand",
            )
            .order_by(
                "asset__asset_tag",
            )
        )