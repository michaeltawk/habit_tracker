from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import IntegrityError

from .forms import HabitForm, HabitEditForm, CustomUserCreationForm
from .models import Habit
from .loops_utils import send_verification_email

import datetime
from decimal import Decimal

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUserCreationForm.Meta.model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_complete.html')
    else:
        return HttpResponse('Activation link is invalid!')

def landing(request):
    return render(request, 'landing.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Activate your Habit Tracker account'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = f"{settings.SITE_URL}/activate/{uid}/{token}/"
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'activation_link': activation_link,
                })

                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                send_verification_email(user.email, activation_link)

                return redirect('signup_complete')
            except IntegrityError:
                form.add_error('email', 'A user with that email already exists. Please choose a different email.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def signup_complete(request):
    return render(request, 'registration/signup_complete.html')

@login_required
def add_habit(request):
    if request.method == 'POST':
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        total_hours = Decimal(hours + minutes / 60).quantize(Decimal('0.01'))

        # Step 1: make a mutable copy of POST
        post_data = request.POST.copy()

        # Step 2: inject computed value
        post_data['hours_spent'] = str(total_hours)

        # Step 3: use modified post_data for the form
        form = HabitForm(post_data)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.date = datetime.date.today()
            habit.save()
        else:
            print("Form errors:", form.errors)

        return redirect('habit_list')
    return redirect('habit_list')

@login_required
def habit_list(request):
    today = datetime.date.today()
    all_habits = Habit.objects.filter(user=request.user).order_by('name', '-date')

    habits_map = {}
    for row in all_habits:
        if row.name not in habits_map:
            habits_map[row.name] = {
                "rows": [],
                "latest": None,
                "total": Decimal('0.00')
            }
        habits_map[row.name]["rows"].append(row)
        habits_map[row.name]["total"] += row.hours_spent

    for name, data in habits_map.items():
        data["rows"].sort(key=lambda r: r.date, reverse=True)
        newest = data["rows"][0]
        if newest.date != today:
            new_row = Habit.objects.create(
                user=request.user,
                name=name,
                date=today,
                hours_spent=Decimal('0.00')
            )
            data["rows"].insert(0, new_row)
            newest = new_row
        data["latest"] = newest

    habits_list = []
    for name, data in habits_map.items():
        newest_row = data["latest"]
        habits_list.append({
            "name": name,
            "pk": newest_row.pk,
            "hours_spent": newest_row.hours_spent,
            "date": newest_row.date,
            "total": data["total"],
        })

    habits_list.sort(key=lambda h: h["name"].lower())

    return render(request, "habit_list.html", {
        "habits": habits_list,
        "hours_range": range(0, 25),
        "minutes_range": range(0, 60),
    })

@login_required
def delete_habit(request, pk):
    habit_row = get_object_or_404(Habit, pk=pk, user=request.user)
    habit_name = habit_row.name

    if request.method == 'POST':
        Habit.objects.filter(user=request.user, name=habit_name).delete()
        return redirect('habit_list')

    return redirect('habit_list')

@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        total_hours = Decimal(hours + minutes / 60).quantize(Decimal('0.01'))

        # Update manually instead of relying on form.save()
        new_name = request.POST.get("name", habit.name)

        habit.name = new_name
        habit.hours_spent = total_hours
        habit.save()

    return redirect('habit_list')

@login_required
def add_hours(request, pk):
    old_habit = get_object_or_404(Habit, pk=pk, user=request.user)

    if request.method == 'POST':
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        hours_val = Decimal(hours + minutes / 60).quantize(Decimal('0.01'))

        today = datetime.date.today()

        if old_habit.date == today:
            old_habit.hours_spent += hours_val
            old_habit.save()
        else:
            Habit.objects.create(
                user=request.user,
                name=old_habit.name,
                date=today,
                hours_spent=hours_val
            )

    return redirect('habit_list')
