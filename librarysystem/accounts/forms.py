from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email","first_name","last_name"]
           
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email","first_name","last_name","is_staff","total_book_due"]
        exclude = ['password']