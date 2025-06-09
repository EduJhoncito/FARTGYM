from django.db import models
from django.contrib.auth.models import User

class ClassSession(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'),
    ]
    name    = models.CharField(max_length=100)
    day     = models.IntegerField(choices=DAY_CHOICES)
    time    = models.TimeField()
    admin   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')

    def __str__(self):
        return f"{self.name} ({self.get_day_display()} @ {self.time})"

class Enrollment(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name='enrollments')
    name    = models.CharField(max_length=100)
    email   = models.EmailField()

    def __str__(self):
        return f"{self.name} → {self.session}"