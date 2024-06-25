from django.urls import path
from .views import CourseDetailView, EnrollActivityView, MyCoursesListView, \
    OptoutActivityView, CoursesListView
from django.contrib.auth.decorators import login_required
from .views.CoursesListView import ProgramCalendarView, AjaxProgramCalendarFeed

urlpatterns = [
    path(
        'activities/my_activities',
        login_required(MyCoursesListView.as_view()),
        name='my_activities'
    ),
    path(
        'program/<slug>',
        CourseDetailView.as_view(),
        name='course'
    ),
    path('program/', CoursesListView.as_view(), name='courses'),
    path('program_calendar/', ProgramCalendarView.as_view(), name='courses_fullcalendar'),
    # AJAX API
    # We are using the default way for FullCalendar to query the events. Because of that, we
    # have to deal with a url with the old style parameters (?blah=12 and so).
    # So the path is everything before the params start, and then in the view we will have to
    # catch the parameters from the GET[].
    path('ajax/program_calendar/', AjaxProgramCalendarFeed.as_view(),
         name="ajax_program_calendar_feed"),
    path('enroll/', EnrollActivityView.as_view(), name='enroll_course'),
    path(
        'activities/<id>/activity_optout',
        OptoutActivityView.as_view(),
        name='activity_optout'
    ),
]
