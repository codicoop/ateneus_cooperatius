import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Room, Reservation, ReservationEquipment, Equipment
from .forms import RoomForm
from apps.coopolis.models import User
from apps.cc_courses.models import CoursePlace


class RoomAdmin(admin.ModelAdmin):
    form = RoomForm
    list_display = ('name', 'color', 'capacity',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "place":
            kwargs["queryset"] = CoursePlace.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Room, RoomAdmin)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "storing_place", )
    readonly_fields = ("storing_place", )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class ReservationEquipmentInlineAdmin(admin.TabularInline):
    model = ReservationEquipment
    extra = 0
    fields = ("equipment", "reservation", "storage_room_field", )
    readonly_fields = ("storage_room_field",)

    def storage_room_field(self, obj):
        if obj.id is None:
            return '-'
        return obj.equipment.storing_place
    storage_room_field.allow_tags = True
    storage_room_field.short_description = 'On es desa'

    def has_change_permission(self, request, obj=None):
        if obj and obj.related_activities.count() > 0:
            return None
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.related_activities.count() > 0:
            return None
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request, obj):
        if obj and obj.related_activities.count() > 0:
            return None
        return super().has_add_permission(request, obj)


class ReservationAdmin(admin.ModelAdmin):
    class Media:
        # Grappelli was not even loading this file (maybe jquery did, internally?)
        # Adding it that way (and having the right order in INSTALLED_APPS injects the file,
        # and then the time pickers use it.
        js = ("grappelli/js/jquery.grp_timepicker.js", 'js/grappellihacks.js',)

    list_display = ('start', 'end', 'room', 'title', 'responsible',)
    readonly_fields = ('created_by', 'created',)
    fields = ('start', 'end', 'room', 'title', 'responsible', 'confirmed',
              'created_by', 'created', 'url', )
    list_filter = ('room', 'start', ('responsible', admin.RelatedOnlyFieldListFilter))
    search_fields = ('title__unaccent', )
    date_hierarchy = 'start'
    inlines = (ReservationEquipmentInlineAdmin, )

    def get_object(self, request, object_id, from_field=None):
        obj = super(ReservationAdmin, self).get_object(request, object_id, from_field)
        if obj and obj.related_activities.count() > 0:
            activity = obj.related_activities.first()
            self.message_user(request, mark_safe(
                "Aquesta reserva no es pot editar directament perquè s'ha generat automàticament.<br />"
                "Per modificar-la o eliminar-la, has de fer-ho a la fitxa de la sessió: "
                f"<a href=\"/admin/cc_courses/activity/{ activity.id }/change/\">{ activity.name }</a>"))
        return obj

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.related_activities.count() > 0:
            return False
        else:
            return super(ReservationAdmin, self).has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.related_activities.count() > 0:
            return self.fields
        else:
            return super(ReservationAdmin, self).get_readonly_fields(request, obj)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if "end" in initial:
            initial["end"] = datetime.datetime.strptime(initial["end"], "%d/%m/%Y %H:%M")
        if "start" in initial:
            initial["start"] = datetime.datetime.strptime(initial["start"], "%d/%m/%Y %H:%M")
        return initial


admin.site.register(Reservation, ReservationAdmin)
