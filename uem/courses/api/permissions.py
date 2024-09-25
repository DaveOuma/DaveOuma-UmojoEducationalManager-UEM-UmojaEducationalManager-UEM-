from rest_framework.permissions import BasePermission

class IsEnrolled(BasePermission):
    """
    Custom permission class to check if a user is enrolled in a course.

    This permission is used to grant access to views only if the user
    is enrolled in the course associated with the object.

    Methods:
        has_object_permission(request, view, obj): 
            Checks if the user has permission to access the given object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determines if the user has permission to access the object.

        Args:
            request (Request): The request object.
            view (View): The view that is being accessed.
            obj (Course): The course object to check for enrollment.

        Returns:
            bool: True if the user is enrolled in the course, False otherwise.
        """
        return obj.students.filter(id=request.user.id).exists()  # Check if user is in the course's student list
