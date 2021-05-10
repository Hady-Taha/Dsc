from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    username = forms.CharField(
        max_length=25,
        min_length=4,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control',}
        )
    )

    
    email=forms.EmailField(required=True,widget=forms.EmailInput(
        attrs={'class': 'form-control mb-2', }
        )
    )

    password=forms.CharField(
        min_length=8, 
        required=True,
        widget=forms.PasswordInput(
            attrs={'type':'password','class':'form-control mb-2',}
            )
        )


    password2 = forms.CharField(
        label="confirm password",
        min_length=8, 
        required=True,
        widget=forms.PasswordInput(
            attrs={'type':'password','class':'form-control mb-2',}
            )
        )



    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password not matche')
        return cd['password2']


    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exists():
            raise forms.ValidationError('this email exists')
        return cd['email']




class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'firstName', 'lastName', 'bio',)


class EditUser(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EditUser, self).__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ('username', 'email',)

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control mb-2', }))


    def clean_email(self):
        cd = self.cleaned_data
        if User.objects.filter(email=cd['email']).exclude(email=self.request.user.email).exists():
            raise forms.ValidationError('this email exists')
        return cd['email']
