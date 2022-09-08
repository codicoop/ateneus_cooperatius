from django.urls import reverse
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings

from apps.facilities_reservations.models import Reservation, Room
from apps.cc_courses.models import Activity


class ReservationsCalendarView(TemplateView):
    template_name = "fullcalendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        context['rooms'] = rooms
        context['legend_activities_outside_color'] = settings.CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE
        return context


class AjaxCalendarFeed(View):
    def get(self, request, *args, **kwargs):
        data = []

        # FullCalendar passes ISO8601 formatted date strings
        try:
            start = parse_datetime(request.GET['start'])
            end = parse_datetime(request.GET['end'])
        except:
            return JsonResponse(data, safe=False)

        events = Reservation.objects.filter(start__gte=start, end__lte=end)
        for event in events:
            title_pieces = []
            if not event.confirmed:
                title_pieces.append("[provisional]")
            title_pieces.append(event.title)
            title_pieces.append(
                "" if event.equipment_summary
                else f"[{event.equipment_summary}]"
            )
            title_pieces.append(
                "" if event.responsible
                else f"[{event.responsible}]"
            )
            event_data = {
                    'title': " ".join(title_pieces),
                    'start': date_to_tull_calendar_format(event.start),
                    'end': date_to_tull_calendar_format(event.end),
                    'color': event.room.color,
                    'url': event.url if event.url else reverse(
                        "admin:facilities_reservations_reservation_change",
                        kwargs={'object_id': event.id},
                    ),
                }
            data.append(event_data)

        # Activity's date_end IS OPTIONAL, so here's the simple solution of filtering only by date_start.
        # TODO: Make date_end mandatory in Activity, to make it fully compatible with the calendar.
        activities = Activity.objects.filter(date_start__gte=start, date_start__lte=end, room=None)
        for activity in activities:
            event_data = {
                    'title': f"[{ activity.place }] { activity }",
                    'start': date_to_tull_calendar_format(
                        make_aware(datetime.combine(activity.date_start, activity.starting_time))),
                    'end': date_to_tull_calendar_format(
                        make_aware(datetime.combine(activity.date_start, activity.ending_time))),
                    'color': settings.CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE,
                    'url': activity.admin_url,
                }
            data.append(event_data)
        return JsonResponse(data, safe=False)


def date_to_tull_calendar_format(date_obj):
    aware_date = timezone.localtime(date_obj)
    return aware_date.strftime("%Y-%m-%dT%H:%M:%S")
