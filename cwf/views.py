from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(request, username=user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'cwf/login.html', {'error': 'Invalid credentials'})
    return render(request, 'cwf/login.html')


@csrf_exempt
def onboard_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usr_name = data.get('usr_name')
        usr_email = data.get('usr_email')
        usr_pswd = data.get('usr_pswd')

        from django.contrib.auth.models import User
        if User.objects.filter(email=usr_email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'})

        user = User.objects.create_user(
            username=usr_email,
            email=usr_email,
            password=usr_pswd,
            first_name=usr_name
        )
        return JsonResponse({'status': 'success', 'message': 'User created successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})