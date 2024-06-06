from django.views import generic
from apps.cc_courses.models import Course
from django.utils import timezone

from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.utils.timezone import make_aware
from django.conf import settings

from apps.facilities_reservations.models import Room
from apps.cc_courses.models import Activity


class ProgramCalendarView(TemplateView):
    template_name = 'courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        context['rooms'] = rooms
        context['legend_activities_outside_color'] = settings.CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE
        return context


class AjaxProgramCalendarFeed(View):
    def get(self, request, *args, **kwargs):
        data = []

        # FullCalendar passes ISO8601 formatted date strings
        try:
            start = parse_datetime(request.GET['start'])
            end = parse_datetime(request.GET['end'])
        except:
            return JsonResponse(data, safe=False)

        activities = Activity.objects.filter(date_start__gte=start, date_end__lte=end)
        for activity in activities:
            activity_data = {
                'title': activity.name,
                'start': date_to_tull_calendar_format(
                    make_aware(datetime.combine(activity.date_start, activity.starting_time))),
                'end': date_to_tull_calendar_format(
                    make_aware(datetime.combine(activity.date_start, activity.ending_time))),
                'color': settings.CALENDAR_COLOR_FOR_ACTIVITIES_OUTSIDE,
                'url': activity.absolute_url,
            }
            data.append(activity_data)
        return JsonResponse(data, safe=False)


def date_to_tull_calendar_format(date_obj):
    aware_date = timezone.localtime(date_obj)
    return aware_date.strftime("%Y-%m-%dT%H:%M:%S")


class CoursesListView(generic.ListView):
    model = Course
    template_name = 'courses.html'

    # queryset = Course.objects.filter(date_start__gte=timezone.now().date())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_courses'] = (
            Course.published.filter(
                activities__date_start__gte=timezone.now().date(),
                activities__publish=True,
            ).distinct()
            .order_by("date_start")
        )
        # context['future_courses'] = context['course_list']
        return context
