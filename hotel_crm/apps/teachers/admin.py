from django.contrib import admin

from hotel_crm.apps.teachers.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
