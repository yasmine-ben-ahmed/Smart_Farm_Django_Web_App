from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.forms import PasswordResetForm


class Form_client(forms.Form):
    firstName = forms.CharField(
        required=True, max_length=client._meta.get_field('firstName').max_length,
        widget=forms.TextInput(attrs={
            'id': "firstName", 'name': "firstName", 'class': "form-control shadow-lg p-6 mb-4 rounded",
            'style': "font-size: 20px; background-color: #DFD9DB;", 'placeholder': 'First Name'
        })
    )

    lastName = forms.CharField(
        required=True, max_length=client._meta.get_field('lastName').max_length,
        widget=forms.TextInput(attrs={
            'id': 'lastName', 'name': 'lastName', 'placeholder': 'Last Name',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    phone = forms.CharField(
        required=True, max_length=client._meta.get_field('phone').max_length,
        widget=forms.TextInput(attrs={
            'id': 'phone', 'name': 'phone', 'placeholder': 'Phone',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    pseudo = forms.CharField(
        required=True, max_length=client._meta.get_field('pseudo').max_length,
        widget=forms.TextInput(attrs={
            'id': 'pseudo', 'name': 'pseudo', 'placeholder': 'Pseudo',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    email = forms.EmailField(
        max_length=client._meta.get_field('email').max_length, required=True,
        widget=forms.EmailInput(attrs={
            'id': 'email', 'name': 'email', 'placeholder': 'Email',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={
            'id': 'password', 'name': 'password', 'placeholder': 'Password',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    confirm_password = forms.CharField(
        required=True, widget=forms.PasswordInput(attrs={
            'id': 'confirm_password', 'name': 'confirm_password', 'placeholder': 'Confirm Password',
            'class': "form-control shadow-lg p-6 mb-4 rounded", 'style': "font-size: 20px; background-color: #DFD9DB;"
        })
    )

    def is_valid(self):
        firstName = self.data['firstName']
        if any(char.isdigit() for char in firstName):
            self.add_error("firstName", "First name is incorrect!")
        
        lastName = self.data['lastName']
        if any(char.isdigit() for char in lastName):
            self.add_error("lastName", "Last name is incorrect!")
        
        pseudo = self.data['pseudo']
        if client.objects.filter(pseudo=pseudo).exists():
            self.add_error("pseudo", "Pseudo already exists!")
        
        email = self.data['email']
        if client.objects.filter(email=email).exists():
            self.add_error("email", "Email already exists!")
        
        phone = self.data['phone']
        if not phone.isdigit():
            self.add_error("phone", "Phone number is incorrect!")
        
        password = self.data['password']
        if len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters long.")
        
        confirm_password = self.data['confirm_password']
        if confirm_password != password:
            self.add_error("confirm_password", "Passwords do not match.")
        
        return super(Form_client, self).is_valid()

    def save(self):
        firstName = self.cleaned_data['firstName']
        lastName = self.cleaned_data['lastName']
        email = self.cleaned_data['email']
        pseudo = self.cleaned_data['pseudo']
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        
        client_instance = client(
            firstName=firstName, lastName=lastName, pseudo=pseudo,
            phone=phone, email=email
        )
        client_instance.save()

        user = User.objects.create_user(pseudo, email, password)
        user.save()


class LoginForm(forms.Form):
    pseudo = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'pseudo', 'name': 'pseudo', 'placeholder': 'Pseudo',
            'class': "form-control shadow-lg p-6 mb-6 rounded", 'style': "font-size: 20px; background-color: white;"
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'password', 'name': 'password', 'placeholder': 'Password',
            'class': "form-control shadow-lg p-6 mb-6 rounded", 'style': "font-size: 20px; background-color: white;"
        })
    )
    
    reset_password = forms.BooleanField(
        required=False, widget=forms.HiddenInput(), initial=False, label='Forgot Password?'
    )

    def is_valid(self, request):
        pseudo = self.data['pseudo']
        password = self.data['password']

        if User.objects.filter(username=pseudo).exists() and client.objects.filter(pseudo=pseudo).exists():
            user = authenticate(request, username=pseudo, password=password)
            if user is None:
                self.add_error("password", "The passwords do not match.")
        else:
            self.add_error("pseudo", "This account does not exist.")
        
        return super(LoginForm, self).is_valid()
