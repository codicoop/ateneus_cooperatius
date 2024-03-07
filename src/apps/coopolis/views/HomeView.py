from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.coopolis.models import Project
from apps.coopolis.views import LoginSignupContainerView


class HomeView(LoginSignupContainerView):
    template_name = "home.html"
    model = Activity

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enrolled_activities"] = ActivityEnrolled.objects.filter(
            activity__date_start__gte=timezone.now().date(),
            user=self.request.user,
            waiting_list=False,
        )
        context["open_projects"] = Project.objects.filter(
            partners=self.request.user,
            stages__stage_state=ProjectStageStatesChoices.OPEN,
        )
        return context
