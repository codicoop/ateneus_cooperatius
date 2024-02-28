from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.coopolis.views import LoginSignupContainerView
from django.utils import timezone
from apps.coopolis.models import Project

class HomeView(LoginSignupContainerView):
    template_name = "home.html"
    model = Activity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enrolled_activities"] = ActivityEnrolled.objects.filter(
            activity__date_start__gte=timezone.now().date(),
            user=self.request.user,
            waiting_list=False,
        )
        context["open_projects"] = Project.objects.filter(
            partners=self.request.user,
        )
        return context
