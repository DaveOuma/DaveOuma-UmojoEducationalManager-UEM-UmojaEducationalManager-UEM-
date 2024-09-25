"""
URL configuration for the educa project, which manages courses and user accounts.

This module maps URL patterns to views for handling courses, authentication, and other functionalities.
"""
import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from courses.views import CourseListView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Login page
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout page
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Password reset
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # After password reset
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Password reset confirm
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # After reset complete
    path('course/', include('courses.urls', namespace='courses')),  # Course URLs
    path('', CourseListView.as_view(), name='course_list'),  # Course list view
    path('students/', include('students.urls', namespace='students')),  # Student URLs
    path('__debug__/', include(debug_toolbar.urls)),  # Debug toolbar for development
    path('api/', include('courses.api.urls', namespace='api')),  # API URLs
    path('chat/', include('chat.urls', namespace='chat')),  # Chat URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development
