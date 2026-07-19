from django.db.models import Max


class CodeGenerator:
    """
    Generates sequential codes.
    """

    @staticmethod
    def generate(model, prefix, field="code", digits=3):

        last = (
            model.objects.filter(**{f"{field}__startswith": prefix})
            .aggregate(Max(field))
            .get(f"{field}__max")
        )

        if not last:
            return f"{prefix}{1:0{digits}}"

        number = int(last.replace(prefix, "")) + 1

        return f"{prefix}{number:0{digits}}"