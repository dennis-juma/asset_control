from django.db import models

from core.utils.slug import generate_unique_slug


class SlugModel(models.Model):
    """
    Automatically generates a unique slug.
    """

    slug = models.SlugField(
        unique=True,
        max_length=255,
        editable=False,
    )

    slug_source = "name"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Generate a unique slug on first save only.
        Existing slugs are preserved during updates.
        """
        if not self.slug:
            value = getattr(self, self.slug_source, "").strip()

            if value:
                self.slug = generate_unique_slug(self, value)

        super().save(*args, **kwargs)