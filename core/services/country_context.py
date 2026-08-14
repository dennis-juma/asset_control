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

    SESSION_KEY = "active_country_id"

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
        """
        Resolve a country explicitly requested by the caller.

        country_id=None means global scope for SUPER_ADMIN.
        """

        if not user.is_authenticated:
            return CountryContext()

        Country = cls._country_model()

        # SUPER_ADMIN can access any active country
        # or all countries when no country is selected.
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

        # Other users can only access countries assigned
        # through UserCountryAccess.
        available = cls.get_available_countries(user)

        if country_id:
            country = available.filter(
                pk=country_id,
            ).first()

            if country:
                return CountryContext(
                    country=country,
                )

        # Default to the first available country.
        country = available.first()

        return CountryContext(
            country=country,
        )

    @classmethod
    def get_session_country_id(cls, request):
        return request.session.get(
            cls.SESSION_KEY,
        )

    @classmethod
    def set_session_country(
        cls,
        request,
        country_id,
    ):
        request.session[cls.SESSION_KEY] = str(
            country_id,
        )

    @classmethod
    def set_global_session(cls, request):
        request.session[cls.SESSION_KEY] = "all"

    @classmethod
    def clear_session_country(cls, request):
        request.session.pop(
            cls.SESSION_KEY,
            None,
        )

    @classmethod
    def resolve_request(cls, request):
        """
        Resolve the active country from the current session.

        The session value is always validated against
        the user's actual country access.
        """

        if not request.user.is_authenticated:
            return CountryContext()

        country_id = cls.get_session_country_id(
            request,
        )

        # SUPER_ADMIN explicitly selected All Countries.
        if country_id == "all":

            if request.user.user_type == "SUPER_ADMIN":
                return CountryContext()

            cls.clear_session_country(request)

            return cls.resolve(
                request.user,
            )

        # No country selected yet.
        if not country_id:
            return cls.resolve(
                request.user,
            )

        # Resolve and validate the selected country.
        context = cls.resolve(
            request.user,
            country_id,
        )

        # If the stored country is no longer accessible,
        # clear it and fall back to the user's default.
        if (
            not context.country
            and request.user.user_type != "SUPER_ADMIN"
        ):
            cls.clear_session_country(request)

            return cls.resolve(
                request.user,
            )

        return context