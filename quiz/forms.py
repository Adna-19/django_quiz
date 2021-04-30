from django.forms.models import inlineformset_factory
from django import forms
from functools import partial
from .models import Question, Answer, Quiz

# DateInput = partial(forms.DateInput, {'class': 'datepicker'})

class QuizForm(forms.ModelForm):
  class Meta:
    model = Quiz
    fields = ['title', 'subject', 'summary', 'score', 'starts_at', 'ends_at']
    widgets = {
      'starts_at': forms.DateInput(attrs={'class': 'datetimepicker'}),
      'ends_at': forms.DateInput(attrs={'class': 'datetimepicker'})
    }

class QuestionForm(forms.ModelForm):
  class Meta:
    model = Question
    fields = ['text', 'score']
    widgets = {
      'text': forms.Textarea(attrs={
        'class': 'form-control w-50 mx-auto', 
        'placeholder': 'Add new Question here...',
        'rows': "5",
        'cols': "40"
      }),
      'score': forms.TextInput(attrs={'class': 'form-control w-50 mx-auto', 'placeholder': 'Add Score here...'})
    }

AnswersFormSet = inlineformset_factory(Question, Answer, fields=['text', 'is_correct'], extra=4)