from django.contrib import admin
from apps.coopolis.choices import ServicesChoices

class SubserviceFilter(admin.SimpleListFilter):
    title = 'Sub-servei'
    parameter_name = 'sub_service'

    def lookups(self, request, model_admin):
        sub_services = [(None, "-")]
        if "service__exact" in request.GET:
            service_id = int(request.GET.get("service__exact"))
            service = ServicesChoices(service_id)
            sub_services = [
                (sub_service.value, sub_service.label)
                for sub_service in service.get_sub_services()
            ]
        return sub_services

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sub_service=self.value())