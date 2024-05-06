from django.views.generic import DetailView
from apps.cc_courses.models import Course, Activity


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activities'] = (
            Activity
            .published.filter(course=context['course'])
            .order_by("date_start", "starting_time", "name")
        )
        # TO DELETE, since 6/5/24:
        # context['enrollment_failed'] = self.request.session.pop(
        #     'enrollment_failed',
        #     False,
        # )
        return context
