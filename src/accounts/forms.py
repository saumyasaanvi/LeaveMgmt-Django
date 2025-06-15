from django import forms
from django.contrib.auth.models import User
from leave.models import Leave 
from django.contrib.auth.forms import UserCreationForm




class UserAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'eg.rajparmar@.com'}))

	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		

	
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['startdate', 'enddate', 'reason', 'leavetype']
        widgets = {
            'startdate': forms.DateInput(attrs={'id': 'id_start_date'}),
            'enddate': forms.DateInput(attrs={'id': 'id_end_date'}),
        }







class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


