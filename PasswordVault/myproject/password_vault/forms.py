from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'form-control', 
            'placeholder':'Enter Your Username'
        })
        self.fields['email'].widget.attrs.update({
            'class':'form-control', 
            'placeholder':'Enter You Email'
        })
        self.fields['password1'].widget.attrs.update({
            'type':'password',
            'class':'form-control password', 
            'placeholder':'Enter Your Password'
        })
        self.fields['password2'].widget.attrs.update({
            'type':'password',
            'class':'form-control password', 
            'placeholder':'Confirm Your Password'
        })
    
        