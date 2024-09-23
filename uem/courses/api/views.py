from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from courses.models import Subject, Course
from courses.api.serializers import SubjectSerializer, CourseSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from courses.api.permissions import IsEnrolled
from courses.api.serializers import CourseWithContentsSerializer


class SubjectListView(generics.ListAPIView):
    """
    View to list all subjects.

    This view retrieves all Subject instances and serializes them
    using the SubjectSerializer.
    """
    queryset = Subject.objects.all()  # Queryset to retrieve all subjects
    serializer_class = SubjectSerializer  # Serializer for the subject data


class SubjectDetailView(generics.RetrieveAPIView):
    """
    View to retrieve details of a specific subject.

    This view retrieves a Subject instance by its primary key and 
    serializes it using the SubjectSerializer.
    """
    queryset = Subject.objects.all()  # Queryset to retrieve all subjects
    serializer_class = SubjectSerializer  # Serializer for the subject data


class CourseEnrollView(APIView):
    """
    View to enroll a user in a course.

    This view allows authenticated users to enroll in a specific 
    course identified by its primary key.
    """
    authentication_classes = [BasicAuthentication]  # Authentication classes
    permission_classes = [IsAuthenticated]  # Permission classes for authenticated users

    def post(self, request, pk, format=None):
        """
        Handle POST request for enrolling a user in a course.

        Args:
            request (Request): The request object containing user information.
            pk (int): The primary key of the course to enroll in.
            format: Optional format for the response.

        Returns:
            Response: A response indicating successful enrollment.
        """
        course = get_object_or_404(Course, pk=pk)  # Retrieve the course or return a 404 error
        course.students.add(request.user)  # Add the user to the course's students
        return Response({'enrolled': True})  # Return a success response


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving courses.

    This viewset provides the standard actions for viewing Course 
    instances, along with additional actions for enrollment and 
    retrieving course contents.
    """
    queryset = Course.objects.all()  # Queryset to retrieve all courses
    serializer_class = CourseSerializer  # Serializer for the course data

    @action(detail=True,
            methods=['post'],
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        """
        Enroll a user in a specific course.

        This action allows authenticated users to enroll in a course 
        identified by its primary key.

        Args:
            request (Request): The request object containing user information.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating successful enrollment.
        """
        course = self.get_object()  # Retrieve the course using the viewset's method
        course.students.add(request.user)  # Add the user to the course's students
        return Response({'enrolled': True})  # Return a success response

    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request, *args, **kwargs):
        """
        Retrieve contents of a specific course.

        This action returns the contents of a course if the user is 
        enrolled in it.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response containing the course contents.
        """
        return self.retrieve(request, *args, **kwargs)  # Use the retrieve method to return course contents
