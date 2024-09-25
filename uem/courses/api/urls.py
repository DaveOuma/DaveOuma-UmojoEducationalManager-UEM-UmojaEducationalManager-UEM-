from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'courses'

# Create a router and register the CourseViewSet
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
    # URL pattern for listing all subjects
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    
    # URL pattern for retrieving details of a specific subject by primary key
    path('subjects/<pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),

    
    # path('courses/<pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll'),

    # Include all routes registered with the router
    path('', include(router.urls)),
]
