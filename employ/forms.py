from django import forms
from .models import Employ_post, Freepost_e, Question, Answer

class EPostForm(forms.ModelForm):
    class Meta:
        model = Employ_post
        fields = ['title','image', 'content', 'employ_shape', 'career',
                  'required_num', 'prefer_condition', 'apply_method',
                  'start_date','end_date']
#

class FreePostForm_e(forms.ModelForm):
    class Meta :
        model = Freepost_e
        fields =['title', 'image', 'content']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields=['title','content','image']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields=['title','content']
