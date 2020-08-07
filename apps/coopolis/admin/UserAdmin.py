import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from constance import config
from django.urls import reverse
from django.utils.safestring import mark_safe

from coopolis.forms import MySignUpAdminForm
from cc_courses.models import ActivityEnrolled
from coopolis_backoffice.custom_mail_manager import MyMailTemplate


class ActivityEnrolledInline(admin.TabularInline):
    class Media:
        js = ('js/grappellihacks.js',)

    model = ActivityEnrolled
    extra = 0
    fields = ('activity', 'course_field', 'user_comments', 'date_enrolled', 'waiting_list',)
    readonly_fields = ('activity', 'course_field', 'user_comments', 'date_enrolled', 'waiting_list',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def course_field(self, obj):
        return obj.activity.course
    course_field.short_description = "Acció"


class UserAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)
        css = {
            'all': ('styles/grappellihacks.css',)
        }

    form = MySignUpAdminForm
    empty_value_display = '(cap)'
    list_display = ('date_joined', 'first_name', 'last_name', 'id_number', 'email', 'project',
                    'enrolled_activities_count')
    search_fields = ('id_number', 'last_name__unaccent', 'first_name__unaccent', 'email', 'phone_number',
                     'cooperativism_knowledge')
    list_filter = ('gender', ('town', admin.RelatedOnlyFieldListFilter), 'district', 'is_staff', 'fake_email',
                   'authorize_communications', )
    fields = ['id', 'first_name', 'last_name', 'surname2', 'gender', 'id_number', 'email', 'fake_email', 'birthdate',
              'birth_place', 'town', 'district', 'address', 'phone_number', 'educational_level',
              'employment_situation', 'discovered_us', 'project_involved', 'cooperativism_knowledge',
              'authorize_communications', 'project', 'is_staff', 'groups',
              'is_active', 'date_joined', 'last_login', ]
    readonly_fields = ['id', 'last_login', 'date_joined', 'project', ]
    actions = ['copy_emails', 'to_csv', ]
    inlines = (ActivityEnrolledInline, )

    def project(self, obj):
        if obj.project:
            return mark_safe(f"<a href=\"../../../project/{ obj.project.id }/change/\">{ obj.project }</a>")
        return None
    project.short_description = 'Projecte'

    def get_fields(self, request, obj=None):
        if request.user.is_superuser and "is_superuser" not in self.fields:
            self.fields.append('is_superuser')

        if not request.user.is_superuser:
            self.readonly_fields.append('groups')

        # If we are adding a new user, don't show these fields:
        if obj is None and 'project' in self.fields:
            self.fields.remove('project')
            self.fields.remove('id')
            self.fields.remove('last_login')

        if obj is None:
            if 'no_welcome_email' not in self.fields:
                self.fields.append('no_welcome_email')
            if 'resend_welcome_email' in self.fields:
                self.fields.remove('resend_welcome_email')
        if obj:
            if 'no_welcome_email' in self.fields:
                self.fields.remove('no_welcome_email')
            if 'resend_welcome_email' not in self.fields:
                self.fields.append('resend_welcome_email')

        return super().get_fields(request, obj)

    def copy_emails(self, request, queryset):
        emails = []
        for user in queryset:
            emails.append(user.email)
        # self.message_user(request, "%s successfully marked as published." % message_bit)
        html = f"<p>La majoria d'aplicacions separen els correus amb comes, però d'altres amb punt i coma; " \
               f"selecciona i copia el que necessitis.</p>" \
               f"<p><em>Recorda: triple clic per seleccionar-ho tot, CTRL+C per copiar i CTRL+V per enganxar. En Mac, " \
               f"CMD en comptes de CTRL.</em></p>" \
               f"<textarea cols=\"150\" rows=\"10\">{', '.join(emails)}</textarea><br><br>" \
               f"<textarea cols=\"150\" rows=\"10\">{'; '.join(emails)}</textarea><br>"
        return HttpResponse(html)
    copy_emails.short_description = 'Copiar tots els e-mails'

    def to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        date = datetime.now().strftime('%Y-%m-%d')
        response['Content-Disposition'] = (
            f"attachment; filename={date}-csv_persones.csv"
        )
        writer = csv.writer(response)
        self.get_csv(queryset, writer)
        return response

    to_csv.short_description = 'Exportar CSV per MailChimp'

    @staticmethod
    def get_csv(users_queryset, writer):
        writer.writerow(
            [
                'Email Address',
                'First Name',
                'Last Name',
                'City',
                'Address',
                'Authorize Newsletter',
            ]
        )
        for user in users_queryset:
            if user.fake_email is True:
                continue
            writer.writerow(
                [
                    user.email,
                    user.first_name,
                    user.surname,
                    user.town if user.town else '',
                    user.address if user.address else '',
                    'yes' if user.authorize_communications else 'no'
                ]
            )

    def save_model(self, request, obj, form, change):
        # Sending welcome e-mail only if we're creating a new account.
        #  and form.cleaned_data['resend_welcome_email']
        send_welcome = (change and form.cleaned_data['resend_welcome_email'] is True) or \
                       (not change and form.cleaned_data['no_welcome_email'] is False)
        if send_welcome:
            self.send_welcome_email(form.cleaned_data['email'])

        super().save_model(request, obj, form, change)

    def send_welcome_email(self, mail_to):
        mail = MyMailTemplate('EMAIL_SIGNUP_WELCOME')
        mail.to = mail_to
        mail.subject_strings = {
            'ateneu_nom': config.PROJECT_FULL_NAME
        }
        mail.body_strings = {
            'ateneu_nom': config.PROJECT_FULL_NAME,
            'url_backoffice': settings.ABSOLUTE_URL,
            'url_accions': f"{settings.ABSOLUTE_URL}{reverse('courses')}",
            'url_projecte': f"{settings.ABSOLUTE_URL}{reverse('project_info')}",
        }
        mail.send()
