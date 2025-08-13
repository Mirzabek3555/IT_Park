from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    school = models.CharField(max_length=200, blank=True)
    grade = models.IntegerField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    total_score = models.IntegerField(default=0)
    tests_taken = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"{self.user.username} profili"
    
    def update_stats(self):
        from tests.models import TestResult
        results = TestResult.objects.filter(user=self.user)
        self.tests_taken = results.count()
        if self.tests_taken > 0:
            self.total_score = sum(result.score for result in results)
            self.average_score = self.total_score / self.tests_taken
        self.save()
