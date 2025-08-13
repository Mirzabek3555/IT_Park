from django.contrib import admin
from .models import Category, Test, Question, Answer, TestResult, UserAnswer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'subject', 'test_type', 'is_active', 'created_at')
    list_filter = ('category', 'subject', 'test_type', 'is_active')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'points', 'order')
    list_filter = ('test', 'points')
    search_fields = ('text',)
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'order')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('text',)

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'percentage', 'time_taken', 'completed_at')
    list_filter = ('test', 'completed_at')
    search_fields = ('user__username', 'user__email', 'test__title')
    readonly_fields = ('completed_at',)

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'points_earned', 'answered_at')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('user__username', 'question__text')
    readonly_fields = ('answered_at',)
