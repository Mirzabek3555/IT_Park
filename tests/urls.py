from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:test_id>/', views.test_detail, name='test_detail'),
    path('<int:test_id>/start/', views.start_test, name='start_test'),
    path('<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('<int:test_id>/result/', views.test_result, name='test_result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
