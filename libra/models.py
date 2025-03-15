import uuid

from django.db import models
import django.core.exceptions
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from datetime import timedelta
import datetime

# default functions

def get_default_poll():
    return Poll.objects.get_or_create(title="Poll")[0].id

def get_default_question():
    return Question.objects.get_or_create(question_text="How are you?")[0].id


# model functions

RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]

class Question(models.Model):
    id = models.UUIDField("unique id", default=uuid.uuid4, primary_key=True)
    # poll = models.ForeignKey(Poll, on_delete=models.CASCADE, default=get_default_poll())
    question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField("date published")
    """
    question_type = models.CharField(
        max_length=20,
        choices=[('multiple_choice', 'Multiple Choice'), ('text', 'Text')],
        default='multiple_choice'
    )
    """
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now()-datetime.timedelta(days=1)


class Choice(models.Model):
    id = models.UUIDField("unique id", default=uuid.uuid4, primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) # see across 

    def __str__(self):
        return self.choice_text
"""
class RatingQuestion(Question):
    scale_type = models.CharField(max_length=50, default="1-10 Rating")
    
    def save(self, *args, **kwargs):
        # First save the question itself
        super().save(*args, **kwargs)
        
        # If this is a new question (no choices yet), create the rating choices
        if not self.choices.exists():
            for value, text in RATING_CHOICES:
                Choice.objects.create(
                    question=self,
                    choice_text=text,
                    votes=0
                )

class YesNoQuestion(Question):
    A question with Yes/No choices
    scale_type = models.CharField(max_length=50, default="Yes/No")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.choices.exists():
            choices = [('Yes', 'Yes'), ('No', 'No')]
            for value, text in choices:
                Choice.objects.create(
                    question=self,
                    choice_text=text,
                    votes=0
                    )
"""
class Data(models.Model):
    id = models.UUIDField("unique id", default=uuid.uuid4, primary_key=True)
    user = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=get_default_question)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_answers(self):
        return Answer.objects.filter(data=self)
        

class Answer(models.Model):
    id = models.UUIDField("unique id", default=uuid.uuid4, primary_key=True)
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
                             
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Username: {self.username}"


