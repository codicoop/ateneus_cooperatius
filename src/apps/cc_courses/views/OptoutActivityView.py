
from django.views import generic
from django.shortcuts import reverse
from apps.cc_courses.models import Activity


class OptoutActivityView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('loginsignup')
        else:
            activity = Activity.objects.get(id=kwargs['id'])
            request.user.enrolled_activities.remove(activity)
            self.url = reverse('my_activities')
        return super().get(request, *args, **kwargs)
