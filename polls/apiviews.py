from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Poll, Question, Choice, Ques
from datetime import datetime
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer, ChoiceSerializer, VoteSerializer, QuestionResultPageSerializer, PollSerializer
from .serializers import QuesSerializer, TextQuestionSerializer, YesNoQuestionSerializer, ChoicesQuestionSerializer

import json

from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def polls_view(request):
    if request.method == 'GET':
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def active_polls_view(request):
    if request.method == 'GET':
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)
    else:
        return Response("Only GET method allowed", status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET', 'PATCH', 'DELETE'])
def poll_detail_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'GET':
        serializer = PollSerializer(poll)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        poll.delete()
        return Response("Poll deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def questions_view(request, poll_id):
    if request.method == 'GET':
        questions = Ques.objects.filter(id=poll_id)
        serializer = QuesSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        poll = get_object_or_404(Poll, pk=poll_id)
        serializer = QuesSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['question_type'] == 1:
                serializer = TextQuestionSerializer(data=request.data)
                if serializer.is_valid():                   
                    ques = serializer.save(poll=poll)
                    return Response(TextQuestionSerializer(ques).data, status=status.HTTP_201_CREATED)      
#                    return Response("Serializer is valid", status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            elif serializer.validated_data['question_type'] == 2:
                serializer = YesNoQuestionSerializer(data=request.data)
                if serializer.is_valid():
                    ques = serializer.save(poll=poll)
                    return Response(YesNoQuestionSerializer(ques).data, status=status.HTTP_201_CREATED)      
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            elif serializer.validated_data['question_type'] == 3:
                serializer = ChoicesQuestionSerializer(data=request.data)
                if serializer.is_valid():
                    ques = serializer.save(poll=poll)
                    return Response(ChoicesQuestionSerializer(ques).data, status=status.HTTP_201_CREATED)      
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response("Question type is not equal one", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#        serializer = QuestionListPageSerializer(data=request.data)
#        if serializer.is_valid():
#            question = serializer.save()
#            return Response(QuestionListPageSerializer(question).data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionListPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionListPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
        choice.votes += 1
        choice.save()
        return Response("Voted")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_result_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)