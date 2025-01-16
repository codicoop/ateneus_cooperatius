from django.conf import settings
from django.urls import re_path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from apps.cc_users.decorators import anonymous_required

from .views import (
    project_stage_characteristics_view,
    project_stage_sessions_view,
    project_stage_initial_petition_view,
    ActivityPollView,
    CoopolisLoginView,
    CoopolisSignUpView,
    CustomPasswordResetView,
    HomeView,
    LoginSignupContainerView,
    ProjectCreateFormView,
    ProjectFormView,
    ProjectInfoView,
    get_sub_services,
    project_stage_attatch_view,
    project_stage_data_view,
    project_stage_start_view,
    project_stage_view,
    db_backup_download_view,
)
from .views.ProjectFormView import project_partner_manage, invitation_partner

urlpatterns = [
    re_path(
        "admin/login",
        RedirectView.as_view(
            pattern_name=settings.LOGIN_URL, permanent=True, query_string=True
        ),
    ),
]

urlpatterns += [
    path("", HomeView.as_view(), name="home"),
    path(
        "users/loginsignup/",
        anonymous_required(LoginSignupContainerView.as_view()),
        name="loginsignup",
    ),
    path(
        "users/login_post/",
        anonymous_required(CoopolisLoginView.as_view()),
        name="login_post",
    ),
    path("users/login/", anonymous_required(CoopolisLoginView.as_view()), name="login"),
    path(
        "users/signup_post",
        anonymous_required(CoopolisSignUpView.as_view()),
        name="signup_post",
    ),
    path(
        "users/signup", anonymous_required(CoopolisSignUpView.as_view()), name="signup"
    ),
    path("grappelli/", include("grappelli.urls")),
    path(
        "admin/docs/",
        TemplateView.as_view(template_name="admin/docs.html"),
        name="docs",
    ),
    path("summernote/", include("django_summernote.urls")),
    path(
        "project/edit/<int:pk>", 
        login_required(ProjectFormView.as_view()),
        name="edit_project"
    ),
    path(
        "project/edit/add-partner/", login_required(project_partner_manage), name="add-partner"
    ),
    path(
        "project/edit/delete-partner/", login_required(project_partner_manage), name="delete_partner"
    ),
    path(
        "project/edit/delete-invitation/", login_required(project_partner_manage), name="delete_invitation"
    ),
    path(
        "project/invitation/<uuid:uuid>/", login_required(invitation_partner), name="invitation_project"
    ),
    path(
        "project/new/",
        login_required(ProjectCreateFormView.as_view()),
        name="new_project",
    ),
    path("project/info/", ProjectInfoView.as_view(), name="project_info"),
    path("project/stage/", project_stage_view, name="project_stage"),
    path(
        "project/stage/start/<int:pk>/",
        project_stage_start_view,
        name="project_stage_start",
    ),
    path(
        "project/stage/data/<int:pk>/",
        project_stage_data_view,
        name="project_stage_data",
    ),
    path(
        "project/stage/attatch/<int:pk>/",
        project_stage_attatch_view,
        name="project_stage_attatch",
    ),
    path(
        "project/stage/initial_petition/<int:pk>/",
        project_stage_initial_petition_view,
        name="project_stage_initial_petition",
    ),
    path(
        "project/stage/characteristics/<int:pk>/",
        project_stage_characteristics_view,
        name="project_stage_characteristics",
    ),
    path("project/stage/sessions/<int:pk>/", project_stage_sessions_view, name="project_stage_sessions"),
    path(
        "email_template_test/",
        TemplateView.as_view(template_name="emails/base.html"),
        name="email_template_test",
    ),
    path(
        "users/password_reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path("reservations/", include("apps.facilities_reservations.urls")),
    path(
        "activities/<uuid:uuid>/poll", ActivityPollView.as_view(), name="activity_poll"
    ),
    path("chained_dropdowns/get_sub_services/", get_sub_services),
    path("admin/", admin.site.urls),
    path("db_backup_download/", db_backup_download_view, name="db_backup_download"),
]
