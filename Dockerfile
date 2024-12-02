# Starting from base Python image
FROM python:3.9.20

# Working directory
WORKDIR /automation

# Copy everything from current directory to Docker "automation" directory
COPY . /automation

# Set environment variable for ChromeDriver
ENV CHROMEDRIVER_DIR=/chromedriver

# Update, upgrade, and install wget & unzip utility
RUN set -ex;\
    apt-get update;\
    apt-get install -y wget unzip

# Download and install Google Chrome
RUN wget -N https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/bin/chromedriver \
    && chown root:root /usr/local/bin/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver

# Specify ChromeDriver Directory in PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Install all necessary dependencies for your project
RUN pip install -r requirements.txt
RUN python3 -m pip install .