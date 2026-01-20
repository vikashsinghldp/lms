from django.contrib import admin

# Register your models here.
from .models import Doubt, Resource, Course, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "is_free")
    list_filter = ("course",)
    ordering = ("course", "order")


@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'is_answered', 'created_at')
    list_filter = ('course', 'is_answered')
    search_fields = ('student__username', 'question')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "resource_type", "uploaded_at")
    list_filter = ("course", "resource_type")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'course_image')
    readonly_fields = ('course_image',)

    def course_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="80" style="border-radius:6px;" />'
        return "No Image"

    course_image.allow_tags = True
    course_image.short_description = 'Image'

