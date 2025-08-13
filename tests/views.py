from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
import json
from .models import Test, Question, Answer, TestResult, UserAnswer, Category
from users.models import Profile

def test_list(request):
    """Testlar ro'yxati"""
    categories = Category.objects.all()
    tests = Test.objects.filter(is_active=True)
    
    # Filtrlash
    category_id = request.GET.get('category')
    subject = request.GET.get('subject')
    
    if category_id:
        tests = tests.filter(category_id=category_id)
    if subject:
        tests = tests.filter(subject=subject)
    
    context = {
        'categories': categories,
        'tests': tests,
        'selected_category': category_id,
        'selected_subject': subject,
    }
    return render(request, 'tests/test_list.html', context)

@login_required
def test_detail(request, test_id):
    """Test batafsil"""
    test = get_object_or_404(Test, id=test_id, is_active=True)
    
    # Foydalanuvchi bu testni yechganmi tekshirish
    existing_result = TestResult.objects.filter(user=request.user, test=test).first()
    
    context = {
        'test': test,
        'existing_result': existing_result,
    }
    return render(request, 'tests/test_detail.html', context)

@login_required
def start_test(request, test_id):
    """Testni boshlash"""
    test = get_object_or_404(Test, id=test_id, is_active=True)
    
    # Foydalanuvchi bu testni yechganmi tekshirish
    existing_result = TestResult.objects.filter(user=request.user, test=test).first()
    if existing_result:
        messages.warning(request, 'Siz bu testni allaqachon yechgansiz!')
        return redirect('test_detail', test_id=test_id)
    
    questions = test.questions.all().order_by('order')
    
    context = {
        'test': test,
        'questions': questions,
    }
    return render(request, 'tests/start_test.html', context)

@login_required
@csrf_exempt
def submit_test(request, test_id):
    """Test natijalarini saqlash"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            test = get_object_or_404(Test, id=test_id)
            
            with transaction.atomic():
                # Test natijasini yaratish
                test_result = TestResult.objects.create(
                    user=request.user,
                    test=test,
                    score=0,
                    max_possible_score=0,
                    time_taken=data.get('time_taken', 0)
                )
                
                total_score = 0
                max_possible_score = 0
                
                # Har bir savolni tekshirish
                for answer_data in data.get('answers', []):
                    question_id = answer_data.get('question_id')
                    selected_answer_id = answer_data.get('selected_answer_id')
                    text_answer = answer_data.get('text_answer', '')
                    
                    question = Question.objects.get(id=question_id)
                    max_possible_score += question.points
                    
                    points_earned = 0
                    is_correct = False
                    
                    if question.test.test_type == 'multiple_choice':
                        if selected_answer_id:
                            selected_answer = Answer.objects.get(id=selected_answer_id)
                            is_correct = selected_answer.is_correct
                            if is_correct:
                                points_earned = question.points
                                total_score += question.points
                    elif question.test.test_type == 'coding':
                        # Kod yozish testlari uchun oddiy tekshirish
                        # Keyinchalik yaxshilanishi mumkin
                        if text_answer.strip():
                            points_earned = question.points
                            total_score += question.points
                            is_correct = True
                    elif question.test.test_type == 'logic':
                        # Mantiqiy masalalar uchun oddiy tekshirish
                        if text_answer.strip():
                            points_earned = question.points
                            total_score += question.points
                            is_correct = True
                    
                    # Foydalanuvchi javobini saqlash
                    UserAnswer.objects.create(
                        user=request.user,
                        question=question,
                        selected_answer_id=selected_answer_id,
                        text_answer=text_answer,
                        is_correct=is_correct,
                        points_earned=points_earned
                    )
                
                # Test natijasini yangilash
                test_result.score = total_score
                test_result.max_possible_score = max_possible_score
                test_result.calculate_percentage()
                test_result.save()
                
                # Foydalanuvchi profilini yangilash
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.update_stats()
                
                return JsonResponse({
                    'success': True,
                    'score': total_score,
                    'max_score': max_possible_score,
                    'percentage': test_result.percentage,
                    'redirect_url': f'/tests/{test_id}/result/'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def test_result(request, test_id):
    """Test natijasi"""
    test_result = get_object_or_404(TestResult, user=request.user, test_id=test_id)
    user_answers = UserAnswer.objects.filter(
        user=request.user,
        question__test_id=test_id
    ).select_related('question', 'selected_answer')
    
    context = {
        'test_result': test_result,
        'user_answers': user_answers,
    }
    return render(request, 'tests/test_result.html', context)

def leaderboard(request):
    """Reyting sahifasi"""
    # Eng yaxshi natijalar
    top_results = TestResult.objects.select_related('user', 'test').order_by('-percentage')[:20]
    
    # Foydalanuvchilar reytingi
    user_rankings = Profile.objects.filter(
        tests_taken__gt=0
    ).select_related('user').order_by('-average_score')[:50]
    
    context = {
        'top_results': top_results,
        'user_rankings': user_rankings,
    }
    return render(request, 'tests/leaderboard.html', context)
