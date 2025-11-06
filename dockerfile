# Use an official Python runtime as a parent image
FROM python:3.9.15

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput
# Expose the port the app runs on
EXPOSE 8000

# Start the Django development server at runtime
# CMD ["python", "manage.py", "runserver"]
CMD ["uvicorn", "habit_tracker_project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
