FROM python:3.6

# Add a user so that app doesnt run as root
RUN adduser --shell /bin/bash --disabled-login --quiet --gecos "" garrison
WORKDIR /home/garrison

# Install Gunicorn server
RUN pip install gunicorn psycopg2

# Copy and install the requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory and other files into the container
COPY app app
COPY migrations migrations
COPY garrison.py config.py boot.sh generate_dispensers.py ./
RUN chmod +x boot.sh

# Create the nessisary environment variables
ENV FLASK_APP garrison.py

# Change ownership of the contents of the directory
RUN chown -R garrison:garrison ./

# Change user
USER garrison

# Expose port 5000
EXPOSE 5000

# Run the startup script
ENTRYPOINT ["./boot.sh"]
