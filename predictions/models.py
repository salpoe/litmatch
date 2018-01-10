from django.db import models
from django.db.models import Count
from accounts.models import Recommendation

class Prediction(models.Model):
    openness = models.FloatField()
    conscientiousness = models.FloatField()
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    neuroticism = models.FloatField()
    jungian_type = models.CharField(max_length=4)

    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True)

    def correlated_reccomendations(self, accuracy=0.25):
        predictions_within_accuracy = Prediction.objects.exclude(user=self.user).filter(
            openness__gt=self.openness - accuracy,
            openness__lt=self.openness + accuracy,
            conscientiousness__gt=self.conscientiousness - accuracy,
            conscientiousness__lt=self.conscientiousness + accuracy,
            extraversion__gt=self.extraversion - accuracy,
            extraversion__lt=self.extraversion + accuracy,
            agreeableness__gt=self.agreeableness - accuracy,
            agreeableness__lt=self.agreeableness + accuracy,
            neuroticism__gt=self.neuroticism - accuracy,
            neuroticism__lt=self.neuroticism + accuracy
        )

        recommended_books = predictions_within_accuracy
        recommended_books = recommended_books.values('user__recommendation')
        recommended_books = recommended_books.annotate(Count("id"))
        recommended_books = recommended_books.order_by('-id__count')[:15]

        return list(recommended_books)
