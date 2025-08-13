from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import News, Direction, Contact, About
from tests.models import TestResult
from django.db.models import Avg, Count, Max
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    """Bosh sahifa"""
    news = News.objects.filter(is_published=True)[:3]
    directions = Direction.objects.filter(is_active=True)[:6]
    about = About.objects.first()
    
    # Reyting statistikasi
    top_users = User.objects.annotate(
        avg_score=Avg('testresult__percentage'),
        test_count=Count('testresult')
    ).filter(test_count__gt=0).order_by('-avg_score')[:5]
    
    context = {
        'news': news,
        'directions': directions,
        'about': about,
        'top_users': top_users,
    }
    return render(request, 'main/home.html', context)

def news_list(request):
    """Yangiliklar ro'yxati"""
    news = News.objects.filter(is_published=True)
    return render(request, 'main/news_list.html', {'news': news})

def news_detail(request, news_id):
    """Yangilik batafsil"""
    news = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'main/news_detail.html', {'news': news})

def directions_list(request):
    """Yo'nalishlar ro'yxati"""
    directions = Direction.objects.filter(is_active=True)
    return render(request, 'main/directions_list.html', {'directions': directions})

def direction_detail(request, direction_id):
    """Yo'nalish batafsil"""
    direction = get_object_or_404(Direction, id=direction_id, is_active=True)
    return render(request, 'main/direction_detail.html', {'direction': direction})

def contact(request):
    """Kontakt sahifasi"""
    contact_info = Contact.objects.first()
    return render(request, 'main/contact.html', {'contact': contact_info})

def about(request):
    """Haqida sahifasi"""
    about_info = About.objects.first()
    return render(request, 'main/about.html', {'about': about_info})

@login_required
def profile(request):
    """Foydalanuvchi profili"""
    user = request.user
    test_results = TestResult.objects.filter(user=user).order_by('-completed_at')
    
    # Statistika
    total_tests = test_results.count()
    avg_score = test_results.aggregate(Avg('percentage'))['percentage__avg'] or 0
    best_score = test_results.aggregate(Max('percentage'))['percentage__max'] or 0
    
    context = {
        'user': user,
        'test_results': test_results,
        'total_tests': total_tests,
        'avg_score': round(avg_score, 1),
        'best_score': round(best_score, 1),
    }
    return render(request, 'main/profile.html', context)
