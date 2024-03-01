from django.contrib import admin

from hotel_crm.apps.students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
