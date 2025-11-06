from django.urls import path
from .views import landing, signup, signup_complete, habit_list, add_habit, edit_habit, delete_habit, add_hours, activate
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', landing, name='landing'),
    path('signup/', signup, name='signup'),
    path('signup-complete/', signup_complete, name='signup_complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('habits/', habit_list, name='habit_list'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('add-habit/', add_habit, name='add_habit'),
    path('habits/<int:pk>/delete/', delete_habit, name='delete_habit'),
    path('habits/<int:pk>/edit/', edit_habit, name='edit_habit'),
    path('habits/<int:pk>/add_hours/', add_hours, name='add_hours'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]
