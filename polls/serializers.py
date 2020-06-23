from rest_framework import serializers
from .models import Poll, Question, Choice, Ques, TextQuestion, YesNoQuestion, ChoicesQuestion

class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Choice.objects.create(**validated_data)

class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    question_type = serializers.CharField()
#    pub_date = serializers.DateTimeField()
#    was_published_recently = serializers.BooleanField(read_only=True)
#    verbose_question_text = serializers.CharField(read_only=True)
#    choices = ChoiceSerializer(many=True, read_only=True)

# DRF serializer.save() calls self.create(self.validated_data)
    def create(self, validated_data):
        return Question.objects.create(**validated_data)

# Add update() implementation on QuestionSerializer
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()

class ChoiceSerializerWithVotes(ChoiceSerializer):
    votes = serializers.IntegerField(read_only=True)

class QuestionResultPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializerWithVotes(many=True, read_only=True)

class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=127)
    start_date = serializers.DateField()
    finish_date = serializers.DateField()
    description = serializers.CharField(max_length=255)
    questions = QuestionListPageSerializer(many=True, read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):       
        for key, value in validated_data.items():
            if key != 'start_date':
                setattr(instance, key, value)
        instance.save()
        return instance

class QuesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    name = serializers.CharField(max_length=127)
    question_type = serializers.IntegerField()
#    question_text = serializers.CharField(max_length=255)

#    def create(self, validated_data):
#        return Ques.objects.create(**validated_data)

class TextQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    name = serializers.CharField(max_length=127)
    question_type = serializers.IntegerField()
    question_text = serializers.CharField(max_length=255)
    def create(self, validated_data):
        return TextQuestion.objects.create(**validated_data)

class YesNoQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    name = serializers.CharField(max_length=127)
    question_type = serializers.IntegerField()
#    yes_no = serializers.BooleanField()
    def create(self, validated_data):
        return YesNoQuestion.objects.create(**validated_data)

class ChoicesQuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)    
    name = serializers.CharField(max_length=127)
    question_type = serializers.IntegerField()
#    yes_no = serializers.BooleanField()
    def create(self, validated_data):
        return ChoicesQuestion.objects.create(**validated_data)
