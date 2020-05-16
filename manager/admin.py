from django.contrib import admin


from .models import Task, Project, AsanaUser

admin.site.register(Task)
admin.site.register(AsanaUser)
admin.site.register(Project)
