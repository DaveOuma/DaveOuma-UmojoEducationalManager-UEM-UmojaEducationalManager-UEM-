from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    # URL for managing the list of courses created by the user.

    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    # URL for creating a new course.

    path('<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    # URL for editing an existing course identified by its primary key (pk).

    path('<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    # URL for deleting a course identified by its primary key (pk).

    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    # URL for updating modules within a course identified by its primary key (pk).

    path('module/<int:module_id>/content/<model_name>/create/', views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    # URL for creating content within a specific module identified by module_id.

    path('module/<int:module_id>/content/<model_name>/<id>/', views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    # URL for updating content within a specific module identified by module_id and content id.

    path('content/<int:id>/delete/', views.ContentDeleteView.as_view(), name='module_content_delete'),
    # URL for deleting content identified by its ID.

    path('module/<int:module_id>/', views.ModuleContentListView.as_view(), name='module_content_list'),
    # URL for listing all contents within a specific module identified by module_id.

    path('module/order/', views.ModuleOrderView.as_view(), name='module_order'),
    # URL for updating the order of modules within a course.

    path('content/order/', views.ContentOrderView.as_view(), name='content_order'),
    # URL for updating the order of contents within a module.

    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),
    # URL for listing courses filtered by a specific subject.

    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    # URL for viewing the details of a specific course identified by its slug.
]
