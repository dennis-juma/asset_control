from django.utils.text import slugify


def generate_unique_slug(instance, value, slug_field="slug"):
    """
    Generate a unique slug for a model instance.
    """

    model = instance.__class__

    slug = slugify(value)
    unique_slug = slug

    counter = 1

    while model.objects.filter(**{slug_field: unique_slug}).exclude(
        pk=instance.pk
    ).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug