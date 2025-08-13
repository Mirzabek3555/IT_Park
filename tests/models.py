from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Test(models.Model):
    TEST_TYPES = [
        ('multiple_choice', 'Ko\'p tanlovli'),
        ('coding', 'Kod yozish'),
        ('logic', 'Mantiqiy masalalar'),
    ]
    
    SUBJECTS = [
        ('programming', 'Dasturlash'),
        ('mathematics', 'Matematika'),
        ('informatics', 'Informatika'),
        ('physics', 'Fizika'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.CharField(max_length=20, choices=SUBJECTS)
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    time_limit = models.IntegerField(help_text='Daqiqalarda', default=30)
    max_score = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.test.title} - {self.text[:50]}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:30]}"

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    max_possible_score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken = models.IntegerField(help_text='Sekundlarda', default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'test']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}%"
    
    def calculate_percentage(self):
        if self.max_possible_score > 0:
            self.percentage = (self.score / self.max_possible_score) * 100
        return self.percentage

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"
