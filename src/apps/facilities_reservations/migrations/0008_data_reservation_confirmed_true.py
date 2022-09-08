from django.db import migrations


def make_previous_events_confirmed(apps, schema_editor):
    print("")
    reservation_model = apps.get_model("facilities_reservations", "Reservation")
    reservation_model.objects.all().update(confirmed=True)
    print("Reserves existents marcades com a confirmades.")


class Migration(migrations.Migration):

    dependencies = [
        ('facilities_reservations', '0007_equipment_reservationequipment'),
    ]

    operations = [
        migrations.RunPython(make_previous_events_confirmed),
    ]
