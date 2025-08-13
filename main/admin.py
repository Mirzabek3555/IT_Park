from django.contrib import admin
from .models import News, Direction, Contact, About

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('order',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email', 'website')
    search_fields = ('address', 'phone', 'email')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'content')
