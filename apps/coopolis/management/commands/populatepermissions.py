# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Creates the user Groups and fills them with the standard permissions.'

    def handle(self, *args, **options):
        self.add_group_permissions()

    @staticmethod
    def add_group_permissions():
        # base user
        group, created = Group.objects.get_or_create(name='Permisos base')
        add_thing = Permission.objects.filter(
            codename__in=['add_logentry', 'change_logentry', 'view_logentry', 'delete_logentry', 'view_permission',
                          'add_town', 'change_town', 'delete_town', 'view_town', 'add_user', 'change_user',
                          'view_user', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Permisos base actualitzats.')

        # formació / sessions
        group, created = Group.objects.get_or_create(name="Gestió d'accions i sessions")
        add_thing = Permission.objects.filter(
            codename__in=['add_activity', 'change_activity', 'delete_activity', 'view_activity', 'add_course',
                          'change_course', 'delete_course', 'view_course', 'add_courseplace', 'change_courseplace',
                          'delete_courseplace', 'view_courseplace', 'view_entity', 'add_organizer',
                          'change_organizer', 'delete_organizer', 'view_organizer', 'add_attachment',
                          'change_attachment', 'delete_attachment', 'view_attachment', 'add_source',
                          'change_source', 'delete_source', 'view_source', 'add_thumbnail', 'change_thumbnail',
                          'delete_thumbnail', 'view_thumbnail', 'add_thumbnaildimensions',
                          'change_thumbnaildimensions', 'delete_thumbnaildimensions', 'view_thumbnaildimensions',
                          'view_activityenrolled', 'delete_activityenrolled', 'change_activityenrolled',
                          'add_activityenrolled']
        )
        group.permissions.set(add_thing)
        group.save()
        print("Permisos del grup Gestió d'accions i sessions actualitzats.")

        # projectes
        group, created = Group.objects.get_or_create(name='Gestió de projectes')
        add_thing = Permission.objects.filter(
            codename__in=['add_project', 'change_project', 'view_project', 'add_projectstagetype',
                          'change_projectstagetype', 'delete_projectstagetype', 'view_projectstagetype',
                          'view_projectstagetype',
                          'add_projectstage', 'change_projectstage', 'delete_projectstage', 'view_projectstage',
                          'add_employmentinsertion', 'change_employmentinsertion', 'delete_employmentinsertion',
                          'view_employmentinsertion']
        )
        group.permissions.set(add_thing)
        group.save()
        print("Permisos del grup Gestió de projectes actualitzats.")

        # gestió de sales
        group, created = Group.objects.get_or_create(name="Afegir o modificar Sales")
        add_thing = Permission.objects.filter(
            codename__in=['add_room', 'change_room', 'delete_room', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Afegir o modificar Sales actualitzats.')

        # gestió de reserves de sales
        group, created = Group.objects.get_or_create(name="Fer i modificar reserves d'espais")
        add_thing = Permission.objects.filter(
            codename__in=['add_reservation', 'change_reservation', 'delete_reservation', ]
        )
        group.permissions.set(add_thing)
        group.save()
        print('Permisos del grup Fer i modificar reserves d\'espais actualitzats.')
