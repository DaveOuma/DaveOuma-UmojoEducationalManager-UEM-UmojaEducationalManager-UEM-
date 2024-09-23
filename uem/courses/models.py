from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string

# Create your models here.
class Subject(models.Model):
    """
    Represents a subject that can have multiple courses.

    Attributes:
    - title: The name of the subject.
    - slug: A unique URL-friendly identifier for the subject.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title']  # Order subjects by title in queries.
        
    def __str__(self):
        """Return the title of the subject as its string representation."""
        return self.title


class Course(models.Model):
    """
    Represents a course belonging to a subject.

    Attributes:
    - owner: The user who created the course.
    - subject: The subject to which the course belongs.
    - title: The name of the course.
    - slug: A unique URL-friendly identifier for the course.
    - overview: A description of the course.
    - created: The timestamp when the course was created.
    - students: The users enrolled in the course.
    """
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True) 
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ['-created']  # Order courses by creation date, newest first.

    def __str__(self):
        """Return the title of the course as its string representation."""
        return self.title


class Module(models.Model):
    """
    Represents a module within a course.

    Attributes:
    - course: The course to which the module belongs.
    - title: The name of the module.
    - description: A description of the module.
    - order: The order of the module within the course.
    """
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']  # Order modules by their defined order.

    def __str__(self):
        """Return the title of the module, prefixed by its order."""
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """
    Represents a piece of content associated with a module.

    Attributes:
    - module: The module to which this content belongs.
    - content_type: The type of content (text, video, image, file).
    - object_id: The ID of the specific content item.
    - item: A generic foreign key to access the specific content instance.
    - order: The order of the content within the module.
    """
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']  # Order content items by their defined order.


class ItemBase(models.Model):
    """
    Abstract base class for content items.

    Attributes:
    - owner: The user who created the content item.
    - title: The name of the content item.
    - created: The timestamp when the content item was created.
    - updated: The timestamp when the content item was last updated.
    """
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This class will not create a database table.

    def __str__(self):
        """Return the title of the content item as its string representation."""
        return self.title
    
    def render(self):
        """
        Render the content item using a specific HTML template.

        Returns:
        str: The rendered HTML for the content item.
        """
        return render_to_string(f'courses/content/{self._meta.model_name}.html', {'item': self})


class Text(ItemBase):
    """
    Represents a text content item.

    Attributes:
    - content: The text content.
    """
    content = models.TextField()


class File(ItemBase):
    """
    Represents a file content item.

    Attributes:
    - file: The file associated with this content item.
    """
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """
    Represents an image content item.

    Attributes:
    - file: The image file associated with this content item.
    """
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """
    Represents a video content item.

    Attributes:
    - url: The URL of the video.
    """
    url = models.URLField()
