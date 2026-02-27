from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('create/', views.create_assignment, name='create_assignment'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('review/<int:assignment_id>/', views.review_submissions, name='review_submissions'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)