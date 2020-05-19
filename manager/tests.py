from unittest.mock import patch

import factory
from django.test import TestCase
from django.contrib.auth.models import User

from .tasks import create_project_task, update_project_task
from .models import Project, Task, AsanaUser


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task


class AsanaUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = AsanaUser


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User


class ProjectTest(TestCase):
    def setUp(self):
        self.test_project_gid = '1176398773557088'
        self.test_project_name = 'Test Project 123'

    @patch("manager.models.create_project_task", autospec=True)
    @patch("manager.tasks.client.projects.create_project", autospec=True)
    def test_create_project(self, asana_client_mock, task_mock):
        """
        Test creating project triggers Asana update.

        """
        project = ProjectFactory(name=self.test_project_name)
        asana_client_mock.return_value = {'gid': self.test_project_gid,
                                          'resource_type': 'project',
                                          'created_at': '2020-05-18T21:16:17.085Z',
                                          'modified_at': '2020-05-18T21:16:17.085Z',
                                          'owner': {'gid': '1176132842428459',
                                                    'resource_type': 'user',
                                                    'name': 'Denis'},
                                          'due_date': None,
                                          'due_on': None,
                                          'current_status': None,
                                          'public': True,
                                          'name': self.test_project_name,
                                          'notes': '',
                                          'archived': False,
                                          'workspace': {'gid': '1176132974660004',
                                                        'resource_type': 'workspace',
                                                        'name': 'Engineering'},
                                          'is_template': False,
                                          'default_view': 'list',
                                          'start_on': None,
                                          'color': None,
                                          'members': [{'gid': '1176132842428459',
                                                       'resource_type': 'user',
                                                       'name': 'Denis'}],
                                          'icon': 'list',
                                          'followers': [{'gid': '1176132842428459',
                                                         'resource_type': 'user',
                                                         'name': 'Denis'}]}
        create_project_task(name=self.test_project_name)
        self.assertTrue(asana_client_mock.called)
        self.assertEqual(Project.objects.get(asana_gid=self.test_project_gid).asana_gid, self.test_project_gid)

    @patch("manager.models.update_project_task", autospec=True)
    @patch("manager.tasks.client.projects.update_project", autospec=True)
    def test_update_project(self, asana_client_mock, task_mock):
        """
        Test updating object triggers Asana update.
        """
        project = ProjectFactory(name=self.test_project_name)
        updated_name = 'new_name'
        asana_client_mock.return_value = {'gid': self.test_project_gid,
                                          'resource_type': 'project',
                                          'created_at': '2020-05-18T22:03:08.245Z',
                                          'modified_at': '2020-05-18T22:07:02.486Z',
                                          'owner': {'gid': '1176132842428459',
                                                    'resource_type': 'user',
                                                    'name': 'Denis'},
                                          'due_date': None,
                                          'due_on': None,
                                          'current_status': None,
                                          'public': True,
                                          'name': updated_name,
                                          'notes': '',
                                          'archived': False,
                                          'workspace': {'gid': '1176132974660004',
                                                        'resource_type': 'workspace',
                                                        'name': 'Engineering'},
                                          'is_template': False,
                                          'default_view': 'list',
                                          'start_on': None,
                                          'color': None,
                                          'members': [{'gid': '1176132842428459',
                                                       'resource_type': 'user',
                                                       'name': 'Denis'}],
                                          'icon': 'list',
                                          'followers': [{'gid': '1176132842428459',
                                                         'resource_type': 'user',
                                                         'name': 'Denis'}]}
        update_project_task(new_name=updated_name, asana_gid=self.test_project_gid)
        asana_client_mock.assert_called_with(name=updated_name, project_gid=self.test_project_gid)
