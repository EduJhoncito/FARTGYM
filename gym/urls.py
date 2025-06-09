from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
    path('dashboard/',views.dashboard,    name='dashboard'),
    path('class-detail/<int:session_id>/', views.class_detail_view, name='class_detail'),
    path('api/sessions/', views.api_sessions, name='api_sessions'),
    path('api/sessions/<int:session_id>/enrollments/', views.api_enrollments, name='api_enrollments'),
]