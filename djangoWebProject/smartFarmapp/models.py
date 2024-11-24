from django.db import models
from django.contrib.auth.models import User
from django import forms

class client(models.Model):
    firstName = models.CharField(max_length=100, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True)
    pseudo = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
        
        return cleaned_data

   
    #user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def save(self, *args, **kwargs):
        if not self.user:
            self.user = User.objects.create_user(self.pseudo, self.email, self.password)

        super().save(*args, **kwargs)
