from django.db import models
from polymorphic.models import PolymorphicModel
import datetime
from django.utils import timezone

class Poll(models.Model):
    name = models.CharField(max_length=127) 
    start_date = models.DateField('date poll started')
    finish_date = models.DateField('date poll finished')
    description = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name
    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.finish_date
    def questions(self):
        if not hasattr(self, '_questions'):
            self._questions = self.question_set.all()
        return self._questions

class Ques(PolymorphicModel):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=127)
    question_type = models.IntegerField()

class TextQuestion(Ques):
    question_text = models.CharField(max_length=255)

class YesNoQuestion(Ques):
#    yes_no = models.BooleanField()
    class Meta:
        verbose_name = "YesNoQuestion"

class ChoicesQuestion(Ques):
    class Meta:
        verbose_name = "ChoicesQuestion"
    
class Choice(models.Model):
    question = models.ForeignKey(ChoicesQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    QUESTION_TYPES = (
                      ('0', 'Text'), 
                      ('1', 'Yes/No'), 
                      ('2', 'Multichoice')
                     )
    question_type = models.IntegerField(QUESTION_TYPES)    
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def verbose_question_text(self):
        return "Question : %s" % (self.question_text)
    def choices(self):
        if not hasattr(self, '_choices'):
            self._choices = self.choice_set.all()
        return self._choices

#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
#
#    def __str__(self):
#        return self.choice_text

#class TextQuestion(Question):

    
