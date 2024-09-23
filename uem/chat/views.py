from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from courses.models import Course

@login_required
def course_chat_room(request, course_id):
    """
    Handles the chat room view for a specific course.

    This view retrieves the course associated with the given course ID 
    for the logged-in user and renders the chat room template.

    Args:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course.

    Returns:
        HttpResponse: Renders the chat room template if the user is enrolled 
        in the course, otherwise returns a forbidden response.
    """
    try:
        # Retrieve course with the given ID, ensuring the user is enrolled
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # User is not a student of the course or the course does not exist
        return HttpResponseForbidden("You do not have access to this course chat room.")

    # Render the chat room template with the course context
    return render(request, 'chat/room.html', {'course': course})
