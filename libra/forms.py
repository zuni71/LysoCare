from django.db import models
from django.forms import ModelForm
from .models import Question, Choice, Data
from django import forms
from django.forms import RadioSelect

"""
class MultipleChoiceQuestionForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            field = question.id
            choices = [(choice.id, choice.choice_text) for choice in question.choices.all()]
            self.fields[field] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                required=True,
                label=question.question_text)
        

class QuestionForm(ModelForm):
    class Meta:
        model = Data
        fields = ["question"]
        labels = {
            "question": "How are you feeling?",
        }
"""
class MultipleChoiceQuestionForm(forms.Form):
    """Form that dynamically creates radio button fields for questions."""
    
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create a radio button field for each question
        for question in questions:
            # Use the question ID as field name
            field_name = f"question_{question.id}"
            
            # Get choices for this question from related model
            choices = [(choice.id, choice.choice_text) 
                      for choice in question.choices.all()]
            
            # Add the field to the form
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=choices,
                widget=RadioSelect,
                required=True
            )
    
    def save(self):
        """Create a data object to store all answers."""
        from .models import Data
        
        # Create a data object to associate with answers
        data = Data.objects.create()
        return data
