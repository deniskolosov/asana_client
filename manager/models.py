import logging

from django.db import models
from .tasks import create_project_task, update_project_task

logger = logging.getLogger(__name__)


class Project(models.Model):
    asana_gid = models.CharField(max_length=256, unique=True, editable=False, null=True)
    name = models.CharField(max_length=256, unique=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Project is created. Run task to create in Asana.
            create_project_task.delay(name=self.name)
        else:
            # Project is updated. Run task to update in Asana
            if self.asana_gid:
                update_project_task.delay(new_name=self.name, asana_gid=self.asana_gid)
            else:
                logger.warning("Can't update project in Asana, no Asana project gid.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Project #{self.name}'


class AsanaUser(models.Model):
    asana_gid = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'User #{self.asana_gid}: {self.name}'


class Task(models.Model):
    asana_gid = models.CharField(max_length=256, unique=True, null=True)
    projects = models.ManyToManyField(Project)
    name = models.CharField(max_length=256, null=True)
    description = models.TextField()
    assignee = models.ForeignKey(AsanaUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Task #{self.asana_gid}: {self.description[:10]}'
