from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from .helpers import auth, predict_from_like_ids
import json

from predictions.models import Prediction, Recommendation

PERSONALITY_TYPES = {
    "ISTJ" : {
        "title" : "The Duty Fulfiller",
        "detail" : "Serious and quiet, interested in security and peaceful living. Extremely thorough, responsible, and dependable. Well-developed powers of concentration. Usually interested in supporting and promoting traditions and establishments. Well-organized and hard working, they work steadily towards identified goals. They can usually accomplish any task once they have set their mind to it."
        },
    "ISTP" : {
        "title" : "The Mechanic",
        "detail" : "Quiet and reserved, interested in how and why things work. Excellent skills with mechanical things. Risk-takers who they live for the moment. Usually interested in and talented at extreme sports. Uncomplicated in their desires. Loyal to their peers and to their internal value systems, but not overly concerned with respecting laws and rules if they get in the way of getting something done. Detached and analytical, they excel at finding solutions to practical problems."
        },
    "ISFJ" : {
        "title" : "The Nurturer",
        "detail" : "Quiet, kind, and conscientious. Can be depended on to follow through. Usually puts the needs of others above their own needs. Stable and practical, they value security and traditions. Well-developed sense of space and function. Rich inner world of observations about people. Extremely perceptive of other's feelings. Interested in serving others."
        },
    "ISFP" : {
        "title" : "The Artist",
        "detail" : "Quiet, serious, sensitive and kind. Do not like conflict, and not likely to do things which may generate conflict. Loyal and faithful. Extremely well-developed senses, and aesthetic appreciation for beauty. Not interested in leading or controlling others. Flexible and open-minded. Likely to be original and creative. Enjoy the present moment."
        },
    "INFJ" : {
        "title" : "The Protector",
        "detail" : "Quietly forceful, original, and sensitive. Tend to stick to things until they are done. Extremely intuitive about people, and concerned for their feelings. Well-developed value systems which they strictly adhere to. Well-respected for their perserverence in doing the right thing. Likely to be individualistic, rather than leading or following."
        },
    "INFP" : {
        "title" : "The Idealist",
        "detail" : "Quiet, reflective, and idealistic. Interested in serving humanity. Well-developed value system, which they strive to live in accordance with. Extremely loyal. Adaptable and laid-back unless a strongly-held value is threatened. Usually talented writers. Mentally quick, and able to see possibilities. Interested in understanding and helping people."
        },
    "INTJ" : {
        "title" : "The Scientist",
        "detail" : "Independent, original, analytical, and determined. Have an exceptional ability to turn theories into solid plans of action. Highly value knowledge, competence, and structure. Driven to derive meaning from their visions. Long-range thinkers. Have very high standards for their performance, and the performance of others. Natural leaders, but will follow if they trust existing leaders."
        },
    "INTP" : {
        "title" : "The Thinker",
        "detail" : "Logical, original, creative thinkers. Can become very excited about theories and ideas. Exceptionally capable and driven to turn theories into clear understandings. Highly value knowledge, competence and logic. Quiet and reserved, hard to get to know well. Individualistic, having no interest in leading or following others."
        },
    "ESTP" : {
        "title" : "The Doer",
        "detail" : "Friendly, adaptable, action-oriented. 'Doers' who are focused on immediate results. Living in the here-and-now, they're risk-takers who live fast-paced lifestyles. Impatient with long explanations. Extremely loyal to their peers, but not usually respectful of laws and rules if they get in the way of getting things done. Great people skills."
        },
    "ESTJ" : {
        "title" : "The Guardian",
        "detail" : "Practical, traditional, and organized. Likely to be athletic. Not interested in theory or abstraction unless they see the practical application. Have clear visions of the way things should be. Loyal and hard-working. Like to be in charge. Exceptionally capable in organizing and running activities. 'Good citizens' who value security and peaceful living."
        },
    "ESFP" : {
        "title" : "The Performer",
        "detail" : "People-oriented and fun-loving, they make things more fun for others by their enjoyment. Living for the moment, they love new experiences. They dislike theory and impersonal analysis. Interested in serving others. Likely to be the center of attention in social situations. Well-developed common sense and practical ability."
        },
    "ESFJ" : {
        "title" : "The Caregiver",
        "detail" : "Warm-hearted, popular, and conscientious. Tend to put the needs of others over their own needs. Feel strong sense of responsibility and duty. Value traditions and security. Interested in serving others. Need positive reinforcement to feel good about themselves. Well-developed sense of space and function."
        },
    "ENFP" : {
        "title" : "The Inspirer",
        "detail" : "Enthusiastic, idealistic, and creative. Able to do almost anything that interests them. Great people skills. Need to live life in accordance with their inner values. Excited by new ideas, but bored with details. Open-minded and flexible, with a broad range of interests and abilities."
        },
    "ENFJ" : {
        "title" : "The Giver",
        "detail" : "Popular and sensitive, with outstanding people skills. Externally focused, with real concern for how others think and feel. Usually dislike being alone. They see everything from the human angle, and dislike impersonal analysis. Very effective at managing people issues, and leading group discussions. Interested in serving others, and probably place the needs of others over their own needs."
        },
    "ENTP" : {
        "title" : "The Visionary",
        "detail" : "Creative, resourceful, and intellectually quick. Good at a broad range of things. Enjoy debating issues, and may be into 'one-up-manship'. They get very excited about new ideas and projects, but may neglect the more routine aspects of life. Generally outspoken and assertive. They enjoy people and are stimulating company. Excellent ability to understand concepts and apply logic to find solutions."
        },
    "ENTJ" : {
        "title" : "The Executive",
        "detail" : "Assertive and outspoken - they are driven to lead. Excellent ability to understand difficult organizational problems and create solid solutions. Intelligent and well-informed, they usually excel at public speaking. They value knowledge and competence, and usually have little patience with inefficiency or disorganization."
        }
}

@method_decorator(login_required, name="dispatch")
class GetPrediction(View):
    template_name = "predictions/index.html"

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'prediction'):
            return redirect('predictions:match')

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        like_ids = json.loads(request.POST['user_likes'])
        token = auth()
        prediction = predict_from_like_ids(token, like_ids)

        jungian_type = sorted(prediction['interpretations'], key=lambda x: str(x['value']))[1]['value']

        model = Prediction.objects.create(
            user=request.user,
            jungian_type=jungian_type,
            openness=prediction['predictions'][4]['value'],
            conscientiousness=prediction['predictions'][1]['value'],
            extraversion=prediction['predictions'][3]['value'],
            agreeableness=prediction['predictions'][0]['value'],
            neuroticism=prediction['predictions'][2]['value'])

        return HttpResponse(status=200)

@method_decorator(login_required, name="dispatch")
class GetLitMatch(View):
    template_name = "predictions/litmatch.html"

    def get(self, request, *args, **kwargs):
        prediction = request.user.prediction
        books = prediction.correlated_reccomendations()
        books = [Recommendation.objects.get(id=book['user__recommendation']) for book in books]

        return render(request, self.template_name, {
            'prediction': prediction,
            'books': books,
            'personality_info': PERSONALITY_TYPES[prediction.jungian_type]
        })
