#!/usr/bin/env python
# -*- coding: utf-8 -*-

# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from django.conf import settings
from cc_lib.utils import get_class_from_route
import inspect


class GenerateFakesCommand(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', '--flush', action='store_true', dest='flush'
        )

    def generated_fake_data(self, objects, model, factory):
        pass

    def fakes_generation_finished(self, fakes):
        pass

    def get_image_fields(self, factory_class):
        from django.db.models.fields.files import ImageFileDescriptor
        return [f[0] for f in inspect.getmembers(factory_class._meta.model) if isinstance(f[1], ImageFileDescriptor)]

    def create_data(self, factory_class, number=50):
        factory = get_class_from_route(factory_class)
        cls_name = factory._meta.model.__name__
        objects = factory.create_batch(size=number)
        self.stdout.write(self.style.SUCCESS(f'Fake data ({number} objects) for {cls_name} model created.'))
        self.generated_fake_data(objects, cls_name, factory)
        return objects, factory

    def download_and_upload_images(self, objects, fields):
        import urllib.request as request
        import tempfile
        from django.core.files import File

        def _download_and_upload_images(obj, prop):
            if getattr(obj, prop) is None:
                return
            url = str(getattr(obj, prop))
            response = request.urlopen(url)
            data = response.read()
            fp = tempfile.TemporaryFile()
            fp.write(data)
            fp.seek(0)
            setattr(obj, prop, File(fp))
            obj.save()

        for field in fields:
            [_download_and_upload_images(obj, field) for obj in objects]
            len(objects) > 0 and self.stdout.write(
                self.style.SUCCESS(f'Updated {field} field image for model {str(objects[0].__class__.__name__)}.')
            )

    def handle(self, *args, **options):
        should_ask = not options['flush']
        Flush().handle(interactive=should_ask, database=DEFAULT_DB_ALIAS, **options)
        assert hasattr(settings, 'FIXTURE_FACTORIES'), """
        You should define FIXTURE_FACTORIES list into the settings file before creating fixtures. 
        """
        factories = settings.FIXTURE_FACTORIES
        factories_dict = {}
        have_images_list = []
        for factory in factories:
            objects, factory_class = self.create_data(*factory)
            factories_dict[factory[0]] = {
                'objects': objects,
                'factory': factory_class
            }
            image_fields = self.get_image_fields(factory_class)
            len(image_fields) > 0 and have_images_list.append((objects, image_fields))
        [self.download_and_upload_images(*elements_with_images) for elements_with_images in have_images_list]
        self.fakes_generation_finished(factories_dict)
