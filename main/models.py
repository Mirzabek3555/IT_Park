from django.db import models
from django.utils.translation import gettext_lazy as _

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Direction(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='directions/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    working_hours = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return "IT Park kontakt ma'lumotlari"

class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
