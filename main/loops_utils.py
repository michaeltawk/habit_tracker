import requests
from django.conf import settings

def send_verification_email(user_email: str, activation_url: str) -> dict:
    """
    Sends your “Activate Account” email via Loops.
    """
    payload = {
        "transactionalId": settings.LOOPS_TRANSACTIONAL_ID,
        "email": user_email,
        "dataVariables": {
            "activation_url": activation_url
        }
    }
    headers = {
        "Authorization": f"Bearer {settings.LOOPS_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(settings.LOOPS_API_URL, json=payload, headers=headers)
    resp.raise_for_status()           # will raise if non-2xx
    return resp.json()               # Loops returns success info

def send_password_reset_email(user_email: str, reset_url: str) -> dict:
    """
    Sends your “Reset Password” email via Loops.
    """
    payload = {
        "transactionalId": settings.LOOPS_PASSWORD_RESET_ID,
        "email": user_email,
        "dataVariables": {
            "reset_url": reset_url
        }
    }
    headers = {
        "Authorization": f"Bearer {settings.LOOPS_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(settings.LOOPS_API_URL, json=payload, headers=headers)
    resp.raise_for_status()           # will raise if non-2xx
    return resp.json()