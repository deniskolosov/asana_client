from asana.error import AsanaError
from django.core.management import BaseCommand

from manager import client, WORKSPACE_GID
from manager.models import AsanaUser


class Command(BaseCommand):
    help = 'Syncronize app users with Asana users.'

    def handle(self, *args, **options):
            asana_users = []
            try:
                asana_users = list(client.users.get_users(workspace=WORKSPACE_GID))
            except AsanaError as e:
                self.stdout.write(self.style.ERROR(f'Error while synchronizing users: {e}'))

            asana_gids = []
            gid_name_map = {}
            for user in asana_users:
                gid = user['gid']
                asana_gids.append(gid)
                gid_name_map[gid] = user['name']

            asana_gids = set(u['gid'] for u in asana_users)
            existing_gids = AsanaUser.objects.values_list('asana_gid', flat=True)
            gids_to_create = asana_gids - set(existing_gids)
            self.stdout.write(f'existing: {existing_gids}, to create: {gids_to_create} resp: {list(asana_users)}')
            if gids_to_create:
                AsanaUser.objects.bulk_create(
                    [AsanaUser(asana_gid=a, name=gid_name_map[a]) for a in list(gids_to_create)]
                )

                self.stdout.write(self.style.SUCCESS(f'Created users: {gid_name_map}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No users were created'))
