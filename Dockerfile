# Starting from base Python image
FROM python:3.9.20

# Working directory
WORKDIR /automation

# Copy everything from current directory to Docker "automation" directory
COPY . /automation

# Upgrade pip
RUN pip install --upgrade pip

# Install all necessary dependencies for your project
RUN pip install -r requirements.txt
RUN python3 -m pip install .