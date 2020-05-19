import logging
from typing import Dict

from asana.error import AsanaError


from asana_client.celery import app
from . import client, WORKSPACE_GID

logger = logging.getLogger(__name__)


@app.task(name='Create project')
def create_project_task(name: str) -> None:
    """
    Create project in Asana.
    """
    response = client.projects.create_project(workspace=WORKSPACE_GID, name=name)
    if response.get('gid'):
        from .models import Project
        Project.objects.filter(name=name).update(asana_gid=response['gid'])
    else:
        logger.error("Could not create project in Asana.")


@app.task(name='Update project')
def update_project_task(new_name: str, asana_gid: str) -> None:
    """
    Update project in Asana.
    """
    try:
        client.projects.update_project(project_gid=asana_gid, name=new_name)
    except AsanaError as e:
        logger.error(f"Error while updating a project: {e}")
    logger.info("Project updated!")


@app.task(name='Create Asana task')
def create_asana_task(
        name: str,
        notes: str,
        assignee_gid: str,
) -> None:
    """
    Create task in Asana.

    """
    from .models import Task
    task = Task.objects.get(name=name)
    project_gids = [p.asana_gid for p in task.projects.all()]
    try:
        resp = client.tasks.create_task(name=name, projects=project_gids, assignee=assignee_gid, notes=notes)
        task.asana_gid = resp.get('gid')
        task.save()
        logger.info(f"Asana response: {resp}")
    except AsanaError as e:
        logger.error(f"Error while creating a task: {e}")


@app.task(name='Update Asana task')
def update_asana_task(**kwargs: Dict[str, str]) -> None:
    """
    Update task in Asana with **kwargs(description, notes, assignee_gid and asana_gid.

    """
    try:
        client.tasks.update_task(**{k: v for k, v in kwargs.items() if v is not None})
        logger.info(f"Asana task {kwargs['task_gid']}: was updated")
    except AsanaError as e:
        logger.error(f"Error while creating a task: {e}")

