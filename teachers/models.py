from django.db import models

from users.models import User


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_teacher=True)


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.is_teacher = True
        super().save(*args, **kwargs)
