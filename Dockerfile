# Set base image (here we use Python 3.9)
FROM python:3.9

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Copy requirements file to working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project to the working directory
COPY . .

# Expose the port the API will run on
EXPOSE 8000

# Command to start the API
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT python manage.py runserver 0.0.0.0:8000



