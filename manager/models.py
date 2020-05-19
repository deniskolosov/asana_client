import logging

from django.db import models
from .tasks import create_project_task, update_project_task

logger = logging.getLogger(__name__)


class Project(models.Model):
    """
    Project representation.
    """
    asana_gid = models.CharField(max_length=256, unique=True, editable=False, null=True) # Asana project id
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

    def __str__(self) -> str:
        return f'Project #{self.name}'


class AsanaUser(models.Model):
    """
    Representation of User instance in Asana. Asana API doesn't allow creating or updating users
    """
    asana_gid = models.CharField(max_length=256, unique=True)  # Asana user id
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f'User #{self.asana_gid}: {self.name}'


class Task(models.Model):
    """
    Representation of Task in Asana, can be in multiple projects and have or don't have an assignee.
    """
    asana_gid = models.CharField(max_length=256, unique=True, null=True)  # Asana user id.
    projects = models.ManyToManyField(Project)
    name = models.CharField(max_length=256, null=True)
    description = models.TextField()
    assignee = models.ForeignKey(AsanaUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'Task #{self.asana_gid}: {self.description[:10]}'
