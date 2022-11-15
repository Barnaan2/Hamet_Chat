from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import OurUserCreationForm,UserForm
from .models import User


# ------------------------------------------------------------------------------------------------------|
#                                                                                   
#   REGISTRATION AND USER MANAGEMENT
# ------------------------------------------------------------------------------------------------------|
def register(request,role="customer"):
    form = OurUserCreationForm()
    if request.method == 'POST':
        form = OurUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat')
        else:
            context = {'form': form}
            return render(request, 'account/register.html', context)
    context = {"form":form}
    return render(request, 'account/register.html', context)



def login_page(request):
    if request.user.is_authenticated:
         return redirect('chat')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'user does not exist')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
        else:
            messages.error(request, 'No matching user  is Found ')
            return redirect('login')
    return render(request, 'account/login.html')


# logout
def logout_page(request):
    logout(request)
    return redirect('index')

