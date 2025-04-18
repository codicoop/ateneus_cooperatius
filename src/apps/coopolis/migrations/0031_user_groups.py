# Generated by Django 2.2.7 on 2019-11-21 16:30

from django.db import migrations
from django.contrib.auth.models import Group, Permission


def add_group_permissions(apps, schema_editor):
    #projectes
    group, created = Group.objects.get_or_create(name='Gestió de projectes')
    # If for some weird reason it's deleted, we recreate it:
    add_thing = Permission.objects.filter(
        codename__in=['add_project', 'change_project', 'view_project', 'add_projectstagetype',
                      'change_projectstagetype', 'delete_projectstagetype', 'view_projectstagetype',
                      'view_projectstagetype',
                      'add_projectstage', 'change_projectstage', 'delete_projectstage', 'view_projectstage',
                      'add_employmentinsertion', 'change_employmentinsertion', 'delete_employmentinsertion',
                      'view_employmentinsertion']
    )
    # Setting all the old and new permissions, to overwrite any potential manual change:
    group.permissions.set(add_thing)
    group.save()
    print("Grup Gestió de projectes actualitzat: afegits permisos a gestió d'Acompanyaments i Insercions Laborals.")


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0030_auto_20191120_2021'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions),
    ]
