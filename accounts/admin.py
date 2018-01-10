from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Recommendation
from django import forms


class UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('first_name', 'last_name', 'email', 'photo', 'birthday', 'location', 'bio')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Recommendation)
