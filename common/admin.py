from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name', 'last_name', 'rut', 'email', 'get_groups', 'superuser')
    list_filter = ('superuser', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'rut', 'email', 'password')}),
        ('Permissions', {'fields': ('groups', 'superuser', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'rut', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('rut', 'email', 'full_name',)
    ordering = ('rut', )
    filter_horizontal = ()

    def get_groups(self, obj):
        return ', '.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''
    get_groups.short_description = 'Groups'

admin.site.register(User, UserAdmin)