import asana
from django.conf import settings

client = asana.Client.access_token(settings.ASANA_TOKEN)

# Get workspace gid from asana
WORKSPACE_GID = list(client.workspaces.get_workspaces())[0]['gid']
