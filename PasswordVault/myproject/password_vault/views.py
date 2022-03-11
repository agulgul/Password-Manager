from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import UserPasswordVault
from .forms import CreateUserForm
from cryptography.fernet import Fernet

fernet = Fernet(settings.KEY)

    
def login_page(request):
    error_message = []
    if request.user.is_authenticated:
        return redirect('password_vault')
    
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.object.get(username=username)
        except:
            messages.error(request, 'User does not exist') 
            error_message = "User does not exist"
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('password_vault')
        else:
            messages.error(request, 'Username or password does not exist')
            error_message = "'Username or password does not exist'"
    context = {'page':page, 'error_message':error_message}
    return render(request, 'login_register.html', context)



def register_page(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('password_vault')
        else:
            messages.error(request, 'An error occured during registration')
    
    if request.user.is_authenticated:
        return redirect('password_vault') 
      
    context = {'form': form}
    return render(request, 'login_register.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    credential = UserPasswordVault.objects.get(pk=pk)
 
    if request.method == 'POST':
        credential.delete()
        return redirect('password_vault')
    context = {'obj':credential}
    return render(request, 'delete.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    credential = UserPasswordVault.objects.get(pk=pk)
    password = fernet.decrypt(credential.password.encode()).decode()
    
    if request.method == 'POST':
        username = request.POST.get('username')         
        passwords = request.POST.get('password')
        url = request.POST.get('url')
        
        encrypted_password = fernet.encrypt(passwords.encode())
       
        credential.user = request.user
        credential.name = username
        credential.password = encrypted_password.decode()
        credential.url = url
        credential.save()
        return redirect('password_vault')

    context = {'obj':credential,'cred':password}
    return render(request, 'update.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    return render(request, 'home.html' )


@login_required(login_url='login')
def create_vault(request):
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       url = request.POST.get('url')
       
       encrypted_password = fernet.encrypt(password.encode())
       query = UserPasswordVault(user=request.user, name=username, password=encrypted_password.decode(), url=url)
       query.save()
       return redirect('password_vault')
   
    return render(request, 'add_password.html')


@login_required(login_url='login')
def passwords_vault(request):
    vault = UserPasswordVault.objects.all()
    if request.method == 'POST':
        password = request.POST.get('password')
        password = fernet.decrypt(password.encode()).decode()
    for password in vault:
        password.password = fernet.decrypt(password.password.encode()).decode()
        
    context = {'vault':vault}
    return render(request,'password_vault.html', context)  

# def show_password(request):
#     password = request.POST.get('password')
#     print(password)    
#     return render(request, 'password_vault.html')
