from django.shortcuts import render, redirect
from uber.forms import CreationFormUser
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def createUser(request):
    form = CreationFormUser()
    
    if request.method == 'POST':
        form = CreationFormUser(request.POST)

        if form.is_valid():
            messages.success(request, 'User created successfully')
            form.save()
            return redirect('uber:login')
            
    return render(
        request,
        'uber/create_user.html',
        {
            'form':form,
            "btn_text":'Create'
        }
    )
    
def login_view(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'{user.username} successfully logged in')
            return redirect('uber:index')
        messages.error(request,'Invalid login')
    
    return render(
        request,
        'uber/login.html',
        {
            'form':form,
            "btn_text":'Login'
        }
    )
 
@login_required(login_url='uber:login')   
def logout_view(request):
    auth.logout(request)
    return redirect('uber:login')