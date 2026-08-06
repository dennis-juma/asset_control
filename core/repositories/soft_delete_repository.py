from core.repositories.base_repository import BaseRepository


class SoftDeleteRepository(BaseRepository):

    @classmethod
    def get_queryset(cls):
        return (
            super()
            .get_queryset()
            .filter(is_deleted=False)
        )

    @classmethod
    def active(cls):
        return cls.get_queryset().filter(is_active=True)

    @classmethod
    def inactive(cls):
        return cls.get_queryset().filter(is_active=False)

    @classmethod
    def soft_delete(cls, instance):

        instance.is_deleted = True

        instance.save()

        return instance

    @classmethod
    def restore(cls, instance):

        instance.is_deleted = False

        instance.save()

        return instance