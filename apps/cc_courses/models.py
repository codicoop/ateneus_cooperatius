from django.db import models
from cc_lib.utils import slugify_model
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.conf import settings
from uuid import uuid4
from apps.cc_courses.exceptions import EnrollToActivityNotValidException
from datetime import date
from easy_thumbnails.fields import ThumbnailerImageField
from coopolis.managers import Published


def upload_path(instance, filename):
    if isinstance(instance, Course):
        return 'course.banner/{0}/banner.png'.format(str(uuid4()), filename)


def activity_signatures_upload_path(instance, filename):
    if isinstance(instance, Activity):
        return 'course.activity_signatures/{0}/{1}'.format(str(uuid4()), filename)


class CoursePlace(models.Model):
    class Meta:
        verbose_name = "lloc"

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    address = models.CharField("adreça", max_length=200)

    def __str__(self):
        return self.name


class Entity(models.Model):
    class Meta:
        verbose_name = "entitat"

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    legal_id = models.CharField("N.I.F.", max_length=9, default="G66622002")
    # TODO: Validate CIF format.

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "acció"
        verbose_name_plural = "accions"
        ordering = ["-date_start"]

    title = models.CharField("títol", max_length=250, blank=False)
    slug = models.CharField(max_length=250, unique=True)
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", null=True, blank=True)
    hours = models.CharField("horaris", blank=False, max_length=200,
                             help_text="Indica només els horaris, sense els dies.")
    description = models.TextField("descripció", null=True)
    publish = models.BooleanField("publicat")
    created = models.DateTimeField(null=True, blank=True)
    banner = ThumbnailerImageField(null=True, upload_to=upload_path, max_length=250, blank=True)
    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc", blank=True,
                              help_text="Aquesta dada de moment és d'ús intern i no es publica.")

    objects = models.Manager()
    published = Published()

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, 'title')

    @property
    def absolute_url(self):
        if self.slug:
            return reverse('course', args=[str(self.slug)])
        return None

    def __str__(self):
        return self.title


class Activity(models.Model):
    class Meta:
        verbose_name = "sessió"
        verbose_name_plural = "sessions"
        ordering = ["-date_start"]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="acció",
                               related_name="activities")
    name = models.CharField("títol", max_length=200, blank=False, null=False)
    objectives = models.TextField("descripció", null=True)
    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc")
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", blank=True, null=True)
    starting_time = models.TimeField("hora d'inici")
    ending_time = models.TimeField("hora de finalització")
    spots = models.IntegerField('places totals', default=0)
    enrolled = models.ManyToManyField("coopolis.User", blank=True, related_name='enrolled_activities',
                                      verbose_name="inscrites")
    entity = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True)
    axis = models.CharField("eix", help_text="Eix de la convocatòria on es justificarà.", choices=settings.AXIS_OPTIONS,
                            null=True, blank=True, max_length=1)
    scanned_signatures = models.FileField("document amb signatures", blank=True, null=True,
                                          upload_to=activity_signatures_upload_path, max_length=250)
    publish = models.BooleanField("publicada", default=True)

    objects = models.Manager()
    published = Published()

    @property
    def remaining_spots(self):
        return self.spots - self.enrolled.count()

    def enroll_user(self, user):
        if user in self.enrolled.all():
            raise EnrollToActivityNotValidException()
        self.enrolled.add(user)
        self.save()

    def __str__(self):
        return self.name

    @property
    def absolute_url(self):
        return self.course.absolute_url

    @property
    def is_past_due(self):
        return date.today() > self.date_start


pre_save.connect(Course.pre_save, sender=Course)
