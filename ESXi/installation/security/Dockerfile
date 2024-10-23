# Use the latest version of Python that supports the latest version of Ansible
FROM python:3.12-slim⁠

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install the necessary Python packages from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the Python scripts to the container
COPY password_encrypt_decrypt.py /app/

# Set the default command to be executed
CMD ["python", "/app/password_encrypt_decrypt.py"]