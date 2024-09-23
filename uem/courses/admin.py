from django.contrib import admin
from .models import Subject, Course, Module

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subject model.

    This class customizes how the Subject model is displayed 
    in the Django admin interface.
    """
    list_display = ['title', 'slug']  # Fields to display in the admin list view
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field from the title


class ModuleInline(admin.StackedInline):
    """
    Inline configuration for the Module model.

    This class allows the Module model to be edited inline 
    within the Course admin interface.
    """
    model = Module  # The model to be displayed inline


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.

    This class customizes how the Course model is displayed 
    in the Django admin interface.
    """
    list_display = ['title', 'subject', 'created']  # Fields to display in the admin list view
    list_filter = ['created', 'subject']  # Filters to apply in the admin interface
    search_fields = ['title', 'overview']  # Fields to search in the admin interface
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field from the title
    inlines = [ModuleInline]  # Include ModuleInline for managing modules within a course
