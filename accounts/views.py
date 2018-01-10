from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from predictions.helpers import auth, predict_from_like_ids
import json

from .models import User, Recommendation
from .forms import UserCreateForm, BookForm

class AccountRegisterView(View):
    template_name = 'registration/register.html'
    form_class = UserCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
            login(request, user)
            return redirect('accounts:profile')
        else:
            return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class AccountProfileView(View):
    template_name = 'registration/profile.html'
    form_class = BookForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(request, self.template_name, { 'form' : form })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # TODO: Notify user of duplicate entry
            model, _ = Recommendation.objects.get_or_create(**form.cleaned_data)
            request.user.recommendation_set.add(model)
            return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name="dispatch")
class RecommendationDetail(View):
    def delete(self, request, *args, **kwargs):
        model = Recommendation.objects.get(pk=self.kwargs['pk'])
        if request.is_ajax:
            request.user.recommendation_set.remove(model)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=402)

class AccountLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
