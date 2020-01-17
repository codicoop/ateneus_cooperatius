"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'Coopolis.back-office.dashboard.CustomIndexDashboard'
"""

from grappelli.dashboard import modules, Dashboard
from django.conf import settings
from django.urls import reverse
from constance import config


class MyDashboard(Dashboard):
    title = "Back-office de "+settings.PROJECT_NAME  # Aquest títol no l'està mostrant enlloc.

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # 'Disabling' reservations module by default, by assigning an empty link module:
        reservations_module_app = modules.LinkList()
        reservations_module_calendar = modules.LinkList()
        if config.ENABLE_ROOM_RESERVATIONS_MODULE:
            reservations_module_app = modules.ModelList(
                    title="Gestió de reserves d'aules i sales",
                    column=1,
                    collapsible=False,
                    models=('facilities_reservations.models.Reservation', 'facilities_reservations.models.Room'),
                )
            reservations_module_calendar = modules.LinkList(
                    title="Calendari de reserves",
                    column=1,
                    collapsible=False,
                    children=(
                        {
                            'title': 'Obrir el calendari (pestanya nova)',
                            'url': reverse('fullcalendar'),
                            'external': False,
                            'target': True,
                        },
                    ),
                )

        self.children.append(modules.Group(
            title=settings.PROJECT_NAME,
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    title='Accions i sessions',
                    column=1,
                    collapsible=False,
                    models=('cc_courses.models.Course', 'cc_courses.models.Activity',),
                ),
                modules.ModelList(
                    title='Acompanyament de projectes',
                    column=1,
                    collapsible=False,
                    models=('coopolis.models.Project', 'coopolis.models.ProjectStage'),
                ),
                reservations_module_app,
                reservations_module_calendar,
                modules.ModelList(
                    title="Gestió d'usuàries",
                    column=1,
                    collapsible=False,
                    models=('coopolis.models.User',),
                ),
                modules.ModelList(
                    title="Exportació de dades per justificacions",
                    column=1,
                    collapsible=False,
                    models=('dataexports.models.DataExports', 'dataexports.models.SubsidyPeriod'),
                ),
                modules.ModelList(
                    title="Gestió de dades",
                    column=1,
                    collapsible=False,
                    models=('cc_courses.models.Organizer', 'cc_courses.models.Entity', 'cc_courses.models.CoursePlace'),
                )
            ]
        ))

        self.children.append(modules.RecentActions(
            title='Accions que has fet recentment',
            column=2,
            limit=5,
        ))

        self.children.append(modules.LinkList(
            title='Enllaços',
            column=3,
            children=(
                ['Gestió de textos del back-office', 'constance/config'],
            )
        ))
