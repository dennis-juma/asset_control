from typing import Generic, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T]):
    """
    Generic repository for CRUD operations.
    """

    model: type[T] = None

    @classmethod
    def get_queryset(cls):
        return cls.model.objects.all()

    @classmethod
    def get(cls, **kwargs):
        return cls.get_queryset().get(**kwargs)

    @classmethod
    def filter(cls, **kwargs):
        return cls.get_queryset().filter(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def update(cls, instance: T, **kwargs):
        for field, value in kwargs.items():
            setattr(instance, field, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, instance: T):
        instance.delete()

    @classmethod
    def exists(cls, **kwargs):
        return cls.filter(**kwargs).exists()

    @classmethod
    def count(cls):
        return cls.get_queryset().count()

    @classmethod
    def first(cls):
        return cls.get_queryset().first()

    @classmethod
    def last(cls):
        return cls.get_queryset().last()

    @classmethod
    def order_by(cls, *fields):
        return cls.get_queryset().order_by(*fields)