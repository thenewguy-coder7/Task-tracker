from django.contrib import admin

from .models import Comment, Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ("title", "status", "priority", "assignee", "due_date")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "summary")
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "assignee", "status", "priority", "due_date")
    search_fields = ("title",)
    list_filter = ("project", "status", "priority")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at")
    search_fields = ("text", "task__title", "author__username")
