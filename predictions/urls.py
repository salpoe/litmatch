from django.contrib import admin
from django.urls import path, include
from .views import GetPrediction, GetLitMatch

app_name = 'predictions'

urlpatterns = [
    path('', GetPrediction.as_view(), name='index'),
    path('match', GetLitMatch.as_view(), name='match'),
]
