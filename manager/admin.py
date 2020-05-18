import logging

from django.contrib import admin

from .models import Task, Project, AsanaUser
from .tasks import update_asana_task, create_asana_task

logger = logging.getLogger(__name__)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = (
        'projects',
        'description',
        'assignee',
        'name',
    )

    def save_model(self, request, obj, form, change):
        """
        Call celery task to update Asana info.

        """

        super().save_model(request, obj, form, change)

        if change and form.changed_data:
            update_asana_task.delay(name=obj.name,
                                    task_gid=obj.asana_gid,
                                    notes=obj.description,
                                    assignee_gid=getattr(obj.assignee, 'asana_gid', ''))
            logger.info(f"changed: {form.changed_data}")
        else:
            logger.info(f" INFO: {obj.projects.all(), obj.description, obj.name}")
            create_asana_task.delay(
                    notes=obj.description,
                    name=obj.name,
                    assignee_gid=getattr(obj.assignee, 'asana_gid', None),
                )


@admin.register(AsanaUser)
class AsanaUserAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'asana_gid'
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )
