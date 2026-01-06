
FROM python:3.11.6

# Copy the application code into the container
COPY . /app

# Create a directory for the .kaggle directory in the Docker image
RUN mkdir -p /root/.kaggle

# Create a file inside .kaggle directory with Kaggle API credentials
RUN echo '{"username":"vamsibatta","key":"34d8ef587a38fc9d3304498dcc8b8dd4"}' > /root/.kaggle/kaggle.json

# Change permissions of kaggle.json file to ensure it's only readable by the owner
RUN chmod 600 /root/.kaggle/kaggle.json

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
