from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

def register(request):
    """Register new User."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New account added successfully. Now you can Sign In')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = dict(form=form)
    return render(request, 'registration/register.html', context)
