from django.db import models
from django.core.validators import ValidationError

from apps.cc_courses.models import CoursePlace
from apps.coopolis.models import User


class Room(models.Model):
    class Meta:
        verbose_name = "sala"
        verbose_name_plural = "sales"
        ordering = ["name", ]

    place = models.ForeignKey(CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc",
                              blank=True)
    name = models.CharField("nom", max_length=250)
    color = models.CharField("color al calendari", max_length=7, default='#e94e1b',
                             help_text="Qualsevol color CSS vàlid, incloent-hi 'red', 'green', etc.")
    capacity = models.IntegerField("capacitat", default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    class Meta:
        verbose_name = "equipament"
        verbose_name_plural = "equipaments"
        ordering = ["name", ]

    name = models.CharField("nom", max_length=100)
    storing_place = models.CharField("on es desa", max_length=250)

    def __str__(self):
        return self.name

    @staticmethod
    def autocomplete_search_fields():
        return ('name__icontains',)


class Reservation(models.Model):
    class Meta:
        verbose_name = "reserva"
        verbose_name_plural = "reserves"

    title = models.CharField("títol", max_length=250)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="sala", related_name='reservations')
    start = models.DateTimeField("data i hora d'inici")
    end = models.DateTimeField("data i hora de finalització")
    responsible = models.ForeignKey(
        User, verbose_name="persona responsable", blank=True, null=True, on_delete=models.SET_NULL,
        related_name='reservations', help_text="Persona de l'equip al càrrec de la reserva. Per aparèixer "
        "al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.")
    url = models.CharField('enllaç web', blank=True, null=True, max_length=250,
                           help_text="En cas d'indicar-se, l'esdeveniment del calendari podrà clicar-se i "
                                     "portarà cap a aquest enllaç.")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="creat per…", null=True)
    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        errors = {}
        """
        If any events of the given room are inside the time span, return false.
        """
        if hasattr(self, "room"):
            q = Reservation.objects.filter(
                models.Q(start__gte=self.start, start__lt=self.end)
                | models.Q(end__gt=self.start, end__lte=self.end)
                | models.Q(start__lte=self.start, end__gte=self.end)
            )

            q = q.filter(room=self.room)

            if self.id:
                q = q.exclude(id=self.id)

            if q.count() > 0:
                errors.update(
                    {
                        "room": ValidationError(
                            "La sala que has seleccionat no està disponible en "
                            "aquest horari."
                        ),
                    }
                )

        if errors:
            raise ValidationError(errors)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super(Reservation, self).save(force_insert, force_update, using, update_fields)

    @property
    def equipment_summary(self):
        """
        For the fullcalendar endpoint to include it in the title.
        """
        if not self.equipments:
            return ""
        equipment_str = [str(x.equipment.name) for x in self.equipments.all()]
        equipment_str.sort()
        return "+".join(equipment_str)


class ReservationEquipment(models.Model):
    class Meta:
        verbose_name = "equipament de la reserva"
        verbose_name_plural = "equipaments de les reserves"
        unique_together = ("equipment", "reservation", )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        verbose_name="equipament",
        related_name="reservations",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        verbose_name="reserva",
        related_name="equipments",
    )

    def __str__(self):
        return f"{self.equipment.name} per la reserva {self.reservation.title}"

    def clean(self):
        super().clean()
        errors = {}
        if hasattr(self, "equipment") and hasattr(self, "reservation"):
            simultaneous_reservations = ReservationEquipment.objects.filter(
                models.Q(
                    reservation__start__gte=self.reservation.start,
                    reservation__start__lt=self.reservation.end,
                )
                | models.Q(
                    reservation__end__gt=self.reservation.start,
                    reservation__end__lte=self.reservation.end,
                )
                | models.Q(
                    reservation__start__lte=self.reservation.start,
                    reservation__end__gte=self.reservation.end,
                )
            )

            simultaneous_reservations = simultaneous_reservations.filter(
                equipment=self.equipment,
            )

            simultaneous_reservations = simultaneous_reservations.exclude(
                reservation=self.reservation,
            )

            if simultaneous_reservations.count() > 0:
                errors.update(
                    {
                        "equipment": ValidationError(
                            "L'equipament seleccionat no està disponible en "
                            "aquest horari."
                        ),
                    }
                )

        if errors:
            raise ValidationError(errors)
