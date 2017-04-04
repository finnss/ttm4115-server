from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Brukernavn', max_length=100)
    password = forms.CharField(label='Passord', max_length=100)
    request = ""

    def __init__(self, request):
        print('request:')
        print(request)
        self.request = request
        self.save()

    def get_user(self):
        return User.objects.get(username=self.request.username)