from django.db import models
from django.db.models import QuerySet

from hotel_crm.apps.users.models import User


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> QuerySet[User]:
        return super().get_queryset(*args, **kwargs).filter(is_student=True)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_student = True
        super().save(*args, **kwargs)
