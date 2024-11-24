from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')


def signUp(request):
    if request.method == 'POST':
        formulaire = Form_client(request.POST)
        if formulaire.is_valid():
            # Form is valid, handle data
            formulaire.enregistrer()
            pseudo = formulaire.cleaned_data['pseudo']  # Access other fields like this
            variable = 'client'  # You can use this variable if needed
            return redirect('home')
        else:
            # If form is invalid, display errors
            return render(request, 'signup.html', {'form': formulaire})
    else:
        # If GET request, render an empty form
        return render(request, 'signup.html', {'form': Form_client()})



def connectasclient(request):
    
    
    if request.method == 'POST':

        if 'reset_password' in request.POST:
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                form.save(
                    request=request,
                    # email_template_name='password_reset_email.html'
                )
                return render(request, 'password_reset_done.html')
        else:
            formulaire = LoginForm(request.POST)
            if formulaire.is_valid(request):
                pseudo = formulaire.cleaned_data['pseudo']
                mot_de_passe = formulaire.cleaned_data['mot_de_passe']
                data = authenticate(request, username=pseudo,
                                    password=mot_de_passe)
                if data is not None:
                    login(request, data)

                    clientp = client.objects.get(pseudo=pseudo)
                    # project = myProject.objects.get(clientp=clientp)
                    
                return redirect('home',pseudo)
            # We pass the form to the template even if it is not valid
            return render(request, 'login_client.html', {'form': formulaire})

    else:
        form = PasswordResetForm()
    # We pass the form to the template for GET requests
    return render(request, 'login_client.html', {'form': LoginForm()})
