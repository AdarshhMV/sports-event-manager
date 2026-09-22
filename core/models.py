from django.db import models
from django.conf import settings

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    is_team_member = models.BooleanField(default=False, verbose_name="Already a team member?")
    past_experience = models.TextField(blank=True, null=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)
    
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'sport')

    def __str__(self):
        return f"{self.user.srn} - {self.sport.name}"

class AuthorityAssignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'sport')
        verbose_name = "Authority Assignment"
        verbose_name_plural = "Authority Assignments"

    def __str__(self):
        return f"{self.user.srn} ({self.user.get_role_display()}) -> {self.sport.name}"