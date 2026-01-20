from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()  # in rupees
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    video_url = models.URLField()  # YouTube / Vimeo / Cloud URL
    duration = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=1)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ["order"]

class Doubt(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    reply = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Resource(models.Model):
    RESOURCE_TYPE = (
        ("note", "Note"),
        ("assignment", "Assignment"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="resources"
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="resources/")
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
