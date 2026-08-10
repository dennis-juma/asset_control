import re


class CodeGenerator:
    """
    Generic sequential code generator.

    Examples:
        CMP001
        BRD001
        CAT001
        MOD001
        AST000001
    """

    @staticmethod
    def generate(
        model,
        prefix: str,
        field_name: str = "code",
        digits: int = 3,
    ) -> str:

        last = (
            model.objects.filter(
                **{f"{field_name}__startswith": prefix}
            )
            .order_by(f"-{field_name}")
            .first()
        )

        if last:
            last_code = getattr(last, field_name)

            match = re.search(r"(\d+)$", last_code)

            if match:
                number = int(match.group(1)) + 1
            else:
                number = 1
        else:
            number = 1

        return f"{prefix}{number:0{digits}d}"