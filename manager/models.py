from django.db import models


class Project(models.Model):
    asana_id = models.IntegerField(unique=True)

    def __str__(self):
        return f'Project #{self.asana_id}'


class AsanaUser(models.Model):
    asana_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'User #{self.asana_id}: {self.name}'


class Task(models.Model):
    asana_id = models.IntegerField(unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    asignee = models.ForeignKey(AsanaUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Task #{self.asana_id}: {self.description[:10]}'
