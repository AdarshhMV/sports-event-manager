from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

def login_view(request):
    if request.method == 'POST':
        srn = request.POST.get('srn')
        password = request.POST.get('password')

        user = authenticate(
            request,
            srn=srn,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'accounts/login.html', {
            'error': 'Invalid SRN or password.'
        })

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')  # <-- Added Full Name
        srn = request.POST.get('srn')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'accounts/signup.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(srn=srn).exists():
            return render(request, 'accounts/signup.html', {
                'error': 'An account with this SRN already exists.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html', {
                'error': 'An account with this email already exists.'
            })

        # Save the full name into the database
        User.objects.create_user(
            srn=srn,
            email=email,
            password=password,
            full_name=full_name  # <-- Passed it here
        )

        return redirect('login')

    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')