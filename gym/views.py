import json
from datetime import datetime

from django.shortcuts       import render, redirect, get_object_or_404
from django.contrib.auth    import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http            import JsonResponse

from .models  import ClassSession, Enrollment
from .forms   import RegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        user     = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        error = "Invalid credentials"
        return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'admin_name': request.user.first_name})

@login_required
def class_detail_view(request, session_id):
    # session_id viene directamente de la URL: /class-detail/4/
    session = get_object_or_404(ClassSession, id=session_id, admin=request.user)
    return render(request, 'class_detail.html', {'session': session})

@login_required
def api_sessions(request):
    if request.method == 'GET':
        sessions = request.user.sessions.all()
        data = [
            {
                'id':   s.id,
                'name': s.name,
                'day':  s.day,
                'time': s.time.strftime('%H:%M')
            }
            for s in sessions
        ]
        return JsonResponse({'sessions': data})

    if request.method == 'POST':
        payload = json.loads(request.body)
        # Convertimos el string "HH:MM" a un objeto datetime.time
        time_obj = datetime.strptime(payload['time'], "%H:%M").time()
        s = ClassSession.objects.create(
            admin=request.user,
            name=payload['name'],
            day=payload['day'],
            time=time_obj
        )
        return JsonResponse({
            'id':   s.id,
            'name': s.name,
            'day':  s.day,
            'time': s.time.strftime('%H:%M')
        })

@login_required
def api_enrollments(request, session_id):
    session = get_object_or_404(ClassSession, id=session_id, admin=request.user)

    if request.method == 'GET':
        data = [
            {'id': e.id, 'name': e.name, 'email': e.email}
            for e in session.enrollments.all()
        ]
        return JsonResponse({'enrollments': data})

    if request.method == 'POST':
        payload = json.loads(request.body)
        e = Enrollment.objects.create(
            session=session,
            name=payload['name'],
            email=payload['email']
        )
        return JsonResponse({'id': e.id, 'name': e.name, 'email': e.email})

    if request.method == 'DELETE':
        payload = json.loads(request.body)
        Enrollment.objects.filter(id=payload['id'], session=session).delete()
        return JsonResponse({'deleted': True})