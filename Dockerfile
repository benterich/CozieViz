# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
