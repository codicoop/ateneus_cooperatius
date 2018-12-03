#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
from factory import fuzzy
from faker import Faker
fake = Faker()
from faker.providers import lorem
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps
import lorem
import random

def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None

class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Activity')

    name = fuzzy.FuzzyText(length=30, chars=lorem.sentence())

class CoursePlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'CoursePlace')
        django_get_or_create = ('name',)

    name = factory.Faker('name')
    address = factory.Faker('address')

class CourseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'CourseCategory')
        django_get_or_create = ('name',)

    name = factory.Faker('name')

class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Course')

    title = factory.Faker('text', max_nb_chars=100, ext_word_list=None)
    date_start = fuzzy.FuzzyDate(datetime.date(2018, 11, 1), datetime.date(2019, 6, 26))
    date_end = fuzzy.FuzzyDate(datetime.date(2019, 6, 27), datetime.date(2019, 12, 26))
    hours = factory.Faker('text', max_nb_chars=15, ext_word_list=None)
    objectives = fake.paragraph(nb_sentences=5, variable_nb_sentences=True, ext_word_list=None)
    published = True
    created = timezone.now()
    #TODO: creator=fuzzy.FuzzyChoice(users) (a generatefakedata)
    #TODO: enrolled (manytomany)
    #TODO: activities (manytomany per error, ha de ser ForeignKey en realitat)
    applications = random.randint(20, 30)

class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('cc_courses', 'Activity')

    name = factory.Faker('text', max_nb_chars=80)
