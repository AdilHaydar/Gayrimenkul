from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


User = get_user_model()
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('username','email', 'admin', 'registration_code')
    list_filter = ('admin','staff','active')
    fieldsets = (
        ('User info', {'fields': ('username','email', 'password','registration_code')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','cep_telefonu','full_name','registration_code', 'password1', 'password2','active','staff','admin')}
        ),
    )
    search_fields = ('email','username','registration_code')
    ordering = ('-last_login',) 
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

