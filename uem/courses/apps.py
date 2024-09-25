from django.apps import AppConfig
import os

class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    path = os.path.join(os.path.dirname(__file__), 'courses')
