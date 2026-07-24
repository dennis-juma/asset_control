from organizations.models import Currency


class CurrencySeeder:
    DEFAULT_CURRENCIES = [
        {
            "code": "TZS",
            "name": "Tanzanian Shilling",
            "symbol": "TSh",
            "is_default": True,
        },
        {
            "code": "KES",
            "name": "Kenyan Shilling",
            "symbol": "KSh",
        },
        {
            "code": "UGX",
            "name": "Ugandan Shilling",
            "symbol": "USh",
        },
        {
            "code": "USD",
            "name": "US Dollar",
            "symbol": "$",
        },
    ]

    @classmethod
    def run(cls, stdout):
        currencies = []

        stdout.write("Creating currencies...")

        for data in cls.DEFAULT_CURRENCIES:
            currency, created = Currency.objects.get_or_create(
                code=data["code"],
                defaults=data,
            )

            currencies.append(currency)

            if created:
                stdout.write(f"  ✓ {currency.code}")
            else:
                stdout.write(f"  • {currency.code} already exists")

        return currencies