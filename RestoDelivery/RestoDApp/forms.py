from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User


class ClientForm(ModelForm):
    class Meta:
        model= Client
        fields = '__all__'
        exclude = ['user']

class PartenaireForm(ModelForm):
    class Meta:
        model= Partenaire
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class':'form-control'})
        self.fields['password2'].widget.attrs.update({'class':'form-control'})
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email','password1','password2']
        widgets={'username':forms.TextInput(attrs={'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


"""class PlatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Plat
        fields = '__all__'
"""


class CategoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Categorie
        fields = '__all__'

