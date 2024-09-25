from rest_framework import serializers
from courses.models import Subject, Course, Module, Content

class SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subject model.

    This serializer handles the serialization and deserialization of 
    Subject instances.
    """
    
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']  # Specify the fields to be included


class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model.

    This serializer manages the serialization and deserialization of 
    Module instances.
    """
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order']  # Specify the fields to be included


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    This serializer handles the serialization of Course instances, 
    including related modules.
    """
    
    modules = ModuleSerializer(many=True, read_only=True)  # Nest ModuleSerializer for related modules

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']  # Specify the fields to be included


class ItemRelatedField(serializers.RelatedField):
    """
    Custom field for related items in content serialization.

    This field is responsible for rendering the related item 
    representation.
    """
    
    def to_representation(self, value):
        """
        Convert the related item to its representation.

        Args:
            value: The related object to be serialized.

        Returns:
            The rendered representation of the related object.
        """
        return value.render()  # Call the render method on the related object


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Content model.

    This serializer manages the serialization and deserialization 
    of Content instances.
    """
    
    item = ItemRelatedField(read_only=True)  # Use the custom ItemRelatedField for item representation

    class Meta:
        model = Content
        fields = ['order', 'item']  # Specify the fields to be included


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Module model with associated contents.

    This serializer includes the contents for each module.
    """
    
    contents = ContentSerializer(many=True)  # Nest ContentSerializer for related contents

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']  # Specify the fields to be included


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model with associated modules and contents.

    This serializer handles the serialization of Course instances,
    including nested modules and their contents.
    """
    
    modules = ModuleWithContentsSerializer(many=True)  # Nest ModuleWithContentsSerializer for related modules

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview', 'created', 'owner', 'modules']  # Specify the fields to be included
