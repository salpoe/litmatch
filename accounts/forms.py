from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from .models import User, Recommendation

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    photo = forms.ImageField(required=False)
    bio = forms.CharField(required=False)
    location = forms.CharField(max_length=64, required=False)
    birthday = forms.DateTimeField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'photo', 'birthday', 'location', 'bio')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.birthday = self.cleaned_data["birthday"]
        user.location = self.cleaned_data["location"]
        user.bio = self.cleaned_data["bio"]
        if commit:
            user.save()
        return user

class BookForm(ModelForm):
    class Meta:
        model = Recommendation
        fields = ['title', 'author']
