from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from loanApp.models import loanCategory,Time ,Percentage_Profit


class LoanCategoryForm(forms.ModelForm):
    class Meta:
        model = loanCategory
        fields = ('loan_name',)


class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ('name',)

class Percentage_Form(forms.ModelForm):
    class Meta:
        model = Percentage_Profit
        fields ='__all__'