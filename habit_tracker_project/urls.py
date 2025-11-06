"""
URL configuration for habit_tracker_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main.forms import LoopsPasswordResetForm
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    # 2) Password-reset email form (uses your custom Loops form)
    path(
      'accounts/password_reset/',
      auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        form_class=LoopsPasswordResetForm
      ),
      name='password_reset'
    ),

    # 3) “We’ve sent you an email” page
    path(
      'accounts/password_reset/done/',
      auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
      ),
      name='password_reset_done'
    ),

    # 4) The link in the email lands here
    path(
      'accounts/reset/<uidb64>/<token>/',
      auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
      ),
      name='password_reset_confirm'
    ),

    # 5) Final “password set! log in” page
    path(
      'accounts/reset/done/',
      auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
      ),
      name='password_reset_complete'
    ),

    # 6) Everything else from django.contrib.auth (login, logout, pw-change…)
    path('accounts/', include('django.contrib.auth.urls')),
]
