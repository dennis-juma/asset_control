from dataclasses import dataclass

from django.apps import apps


@dataclass(frozen=True)
class CountryContext:
    """
    Represents the active country scope for the current user.

    country=None means all countries.
    """

    country: object | None = None

    @property
    def is_global(self):
        return self.country is None


class CountryContextService:

    @staticmethod
    def _country_model():
        return apps.get_model(
            "organizations",
            "Country",
        )

    @staticmethod
    def _access_model():
        return apps.get_model(
            "accounts",
            "UserCountryAccess",
        )

    @classmethod
    def get_available_countries(cls, user):

        Country = cls._country_model()

        if not user.is_authenticated:
            return Country.objects.none()

        if user.user_type == "SUPER_ADMIN":
            return Country.objects.filter(
                is_active=True,
            ).order_by("name")

        return Country.objects.filter(
            user_access__user=user,
            is_active=True,
        ).distinct().order_by("name")

    @classmethod
    def can_access_country(
        cls,
        user,
        country,
    ):

        if not user.is_authenticated:
            return False

        if user.user_type == "SUPER_ADMIN":
            return True

        UserCountryAccess = cls._access_model()

        return UserCountryAccess.objects.filter(
            user=user,
            country=country,
        ).exists()

    @classmethod
    def resolve(
        cls,
        user,
        country_id=None,
    ):

        if not user.is_authenticated:
            return CountryContext()

        Country = cls._country_model()

        if user.user_type == "SUPER_ADMIN":

            if not country_id:
                return CountryContext()

            country = Country.objects.filter(
                pk=country_id,
                is_active=True,
            ).first()

            if not country:
                return CountryContext()

            return CountryContext(
                country=country,
            )

        available = cls.get_available_countries(user)

        if country_id:
            country = available.filter(
                pk=country_id,
            ).first()

            if country:
                return CountryContext(
                    country=country,
                )

        country = available.first()

        return CountryContext(
            country=country,
        )