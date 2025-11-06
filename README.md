# Habit Tracker

A web application for tracking daily habits, built with Django.

## Features

- User registration and email activation
- Secure login/logout and password reset
- Add, edit, and delete habits
- Track hours spent on each habit per day
- Responsive UI with custom CSS

## Technologies

- Python 3.9+
- Django
- PostgreSQL
- Docker support

## Setup Instructions

### 1. Clone the repository

```
git clone <repo-url>
cd HabitTracker-main
```

### 2. Install dependencies

Create a virtual environment and install requirements:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```
SECRET_KEY=your-secret-key
DATABASE_NAME=your-db-name
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
LOOPS_API_KEY=your-loops-api-key
LOOPS_API_URL=your-loops-api-url
LOOPS_TRANSACTIONAL_ID=your-loops-transactional-id
LOOPS_PASSWORD_RESET_ID=your-loops-password-reset-id
SITE_URL=https://your-site-url.com
```

Update `habit_tracker_project/settings.py` to read these from environment variables.

### 4. Database setup

Create a PostgreSQL database and user matching your `.env` settings.
Run migrations:

```
python manage.py migrate
```

### 5. Run the development server

```
python manage.py runserver
```

### 6. Docker (optional)

Build and run the app using Docker:

```
docker build -t habit-tracker .
docker run -p 8000:8000 habit-tracker
```

## Folder Structure

- `habit_tracker_project/` - Django project settings
- `main/` - Main app (models, views, forms, etc.)
- `static/` - CSS files
- `templates/` - HTML templates

## Security Notes

- Do not commit sensitive credentials to source control.
- Use environment variables for all secrets and API keys.

## License

MIT
