from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Poll, Question, Choice
from datetime import datetime
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer, ChoiceSerializer, VoteSerializer, QuestionResultPageSerializer, PollSerializer

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
def questions_view(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionListPageSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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