from django.contrib import admin
from django.urls import path
from core.views import dashboard, sports_registration, my_registrations, profile, manage_team, toggle_team_status, my_team
from accounts.views import login_view, signup_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='home'),
    path('register/', sports_registration, name='sports_registration'),
    path('my-registrations/', my_registrations, name='my_registrations'),
    path('profile/', profile, name='profile'),
    path('manage-team/', manage_team, name='manage_team'),
    path('toggle-status/<int:reg_id>/', toggle_team_status, name='toggle_team_status'),
    path('my-team/', my_team, name='my_team'),
    
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]