from django.shortcuts import render, redirect
from uber.forms import CreationFormUser
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm

def createUser(request):
    form = CreationFormUser()
    
    if request.method == 'POST':
        form = CreationFormUser(request.POST)

        if form.is_valid():
            messages.success(request, 'Usuário criado com sucesso')
            form.save()
            return redirect('uber:index')
            
    return render(
        request,
        'uber/create_user.html',
        {
            'form':form,
            "btn_text":'Criar'
        }
    )
    
def login_view(request):
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, f'{user.username} Logado com sucesso')
            return redirect('uber:index')
        messages.error(request,'Login inválido')
    
    return render(
        request,
        'uber/login.html',
        {
            'form':form,
            "btn_text":'Login'
        }
    )
    
def logout_view(request):
    auth.logout(request)
    return redirect('uber:login')