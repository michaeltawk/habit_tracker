from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Habit
from .loops_utils import send_password_reset_email
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(required=True, max_length=30, help_text="Required. Enter your first name.")
    last_name = forms.CharField(required=True, max_length=30, help_text="Required. Enter your last name.")

    class Meta:
        model = User
        # We are not including a separate username field because we'll use email as username.
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with that email already exists. Please choose a different email."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set username to email to satisfy the default user model
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'hours_spent']

class HabitEditForm(forms.ModelForm):
    """Used for editing an existing habit. Also excludes date."""
    class Meta:
        model = Habit
        fields = ['name', 'hours_spent'] 

class LoopsPasswordResetForm(PasswordResetForm):
    def save(
        self,
        domain_override=None,
        subject_template_name=None,
        email_template_name=None,
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None
    ):
        """
        Generates a UID and token for each matching user and fires off
        the reset email through Loops.
        """
        # Iterate over all users matching the submitted email
        for user in self.get_users(self.cleaned_data["email"]):
            # 1. Create the URL-safe base64 UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # 2. Generate a one-time use token
            token = token_generator.make_token(user)

            # 3. Reverse the named URL for the confirm view
            reset_path = reverse(
                "password_reset_confirm",
                kwargs={"uidb64": uid, "token": token}
            )

            # 4. Build the full URL (e.g. "https://habit-trackers.com/accounts/reset/…/")
            reset_link = f"{settings.SITE_URL}{reset_path}"

            # 5. Send the email via Loops
            send_password_reset_email(user.email, reset_link)