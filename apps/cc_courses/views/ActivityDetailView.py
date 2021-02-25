from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from cc_courses.models import Activity


class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'activity.html'

    def get(self, request, *args, **kwargs):
        ret = super(ActivityDetailView, self).get(request, *args, **kwargs)
        if (
                (
                    not self.object.instructions
                    and not self.object.videocall_url
                    and len(self.object.resources.all()) == 0
                )
                or request.user not in self.object.confirmed_enrollments.all()
        ):
            return HttpResponseRedirect(reverse('my_activities'))
        return ret
