from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from courses.models import Course

@login_required
def course_chat_room(request, course_id):
    try:
        # Retrieve course with the given ID, joined by the current user
        course = request.user.courses_joined.get(id=course_id)
    except Course.DoesNotExist:
        # User is not a student of the course or the course does not exist
        return HttpResponseForbidden("You do not have access to this course chat room.")

    return render(request, 'chat/room.html', {'course': course})
