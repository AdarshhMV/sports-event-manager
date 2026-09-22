from django.contrib import admin
from .models import Sport, Registration, AuthorityAssignment

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport', 'branch', 'year', 'registered_at')
    list_filter = ('sport', 'year', 'is_team_member')
    search_fields = ('user__srn', 'branch')

@admin.register(AuthorityAssignment)
class AuthorityAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'sport')
    list_filter = ('sport',)
    search_fields = ('user__srn',)  