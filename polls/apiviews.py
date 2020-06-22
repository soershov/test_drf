from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Question
from datetime import datetime

@csrf_exempt
def questions_view(request):
    if request.method == 'GET':
        return HttpResponse("Not Implemented, try POST instead")
    elif request.method == 'POST':
        question_text = request.POST['question_text']
        pub_date = datetime.strptime(request.POST['pub_date'], '%Y-%m-%d')
        Question.objects.create(question_text=question_text, pub_date=pub_date)
        return HttpResponse("Question created", status=201)