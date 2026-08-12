from django.core.paginator import Paginator

from assets.models.asset_attachment import AssetAttachment


class AssetAttachmentRepository:

    # =====================================================
    # Create
    # =====================================================

    def create(
        self,
        attachment: AssetAttachment,
    ) -> AssetAttachment:

        attachment.save()

        return attachment

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        pk,
    ) -> AssetAttachment:

        return AssetAttachment.objects.select_related(
            "asset",
        ).get(
            pk=pk,
        )

    # =====================================================
    # List
    # =====================================================

    def list(
        self,
        asset,
        page=1,
    ):

        queryset = (
            AssetAttachment.objects
            .filter(
                asset=asset,
            )
            .select_related(
                "asset",
            )
            .order_by(
                "-created_at",
            )
        )

        paginator = Paginator(
            queryset,
            20,
        )

        return paginator.get_page(page)

    # =====================================================
    # Update
    # =====================================================

    def update(
        self,
        attachment: AssetAttachment,
    ) -> AssetAttachment:

        attachment.save()

        return attachment

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        attachment: AssetAttachment,
    ) -> None:

        attachment.delete()