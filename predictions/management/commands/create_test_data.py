import csv
import os
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.decorators import method_decorator
from mixer.backend.django import mixer

from accounts.models import User, Recommendation
from predictions.models import Prediction

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_users(self):
        self.users = [mixer.blend(User) for _ in range(100)]

    def _create_predictions(self):
        for user in self.users:
            Prediction.objects.create(
                openness=random.random(),
                conscientiousness=random.random(),
                extraversion=random.random(),
                agreeableness=random.random(),
                neuroticism=random.random(),
                jungian_type='ESFJ',
                user=user
            )

    def _create_recommendations(self):
        csv_data = os.path.join(os.path.dirname(__file__), 'data', 'reading_list.csv')

        with open(csv_data, 'r') as f:
            books = list(csv.reader(f))

            for user in self.users:
                while len(user.recommendation_set.all()) <= 10:
                    book = random.choice(books)

                    recommendation, _ = Recommendation.objects.get_or_create(
                        title=book[0],
                        author=book[1]
                    )

                    if not user.recommendation_set.filter(pk=recommendation.pk).exists():
                        user.recommendation_set.add(recommendation)

    @method_decorator(transaction.atomic)
    def handle(self, *args, **options):
        self._create_users()
        self._create_predictions()
        self._create_recommendations()
