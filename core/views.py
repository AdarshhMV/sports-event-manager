from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Registration, AuthorityAssignment
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def dashboard(request):
    return render(request, 'home.html')

@login_required
def sports_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            
            if Registration.objects.filter(user=request.user, sport=registration.sport).exists():
                form.add_error('sport', 'You are already registered for this sport.')
            else:
                registration.save()
                return redirect('my_registrations') 
    else:
        form = RegistrationForm()
        
    return render(request, 'registration.html', {'form': form})

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user).order_by('-registered_at')
    return render(request, 'my_registrations.html', {'registrations': registrations})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def manage_team(request):
    # Security check: Kick out regular students
    if request.user.role == 'STUDENT':
        return redirect('home')
        
    # Fetch sports assigned to this specific authority
    assignments = AuthorityAssignment.objects.filter(user=request.user)
    managed_sports = [assignment.sport for assignment in assignments]
    
    # Fetch all students registered for those specific sports
    registrations = Registration.objects.filter(sport__in=managed_sports).order_by('sport__name', '-registered_at')
    
    return render(request, 'manage_team.html', {
        'managed_sports': managed_sports,
        'registrations': registrations
    })

@login_required
def toggle_team_status(request, reg_id):
    if request.method == 'POST' and request.user.role != 'STUDENT':
        # Find the specific registration
        registration = get_object_or_404(Registration, id=reg_id)
        
        # Verify this captain is actually assigned to this sport
        if AuthorityAssignment.objects.filter(user=request.user, sport=registration.sport).exists():
            # Flip the status and save
            registration.is_team_member = not registration.is_team_member
            registration.save()
            
    return redirect('manage_team')

@login_required
def my_team(request):
    team_rosters = {} 
    
    if request.user.role == 'STUDENT':
        # Find sports where this specific student was selected
        my_selections = Registration.objects.filter(user=request.user, is_team_member=True)
        sports_involved = [reg.sport for reg in my_selections]
    else:
        # Find sports assigned to this captain/coach
        assignments = AuthorityAssignment.objects.filter(user=request.user)
        sports_involved = [assignment.sport for assignment in assignments]
        
    # Build the roster of approved students for each relevant sport
    for sport in sports_involved:
        selected_members = Registration.objects.filter(sport=sport, is_team_member=True).order_by('user__srn')
        team_rosters[sport] = selected_members
        
    return render(request, 'my_team.html', {'team_rosters': team_rosters})