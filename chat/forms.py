from django import forms
from django.forms import ModelForm, Textarea



class User_search_form(forms.Form):
    companion = forms.CharField(label='Имя пользователя', max_length=100)