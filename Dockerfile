FROM apache/airflow:latest-python3.12

USER root

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxi6 \
    libgconf-2-4 \
    libasound2 \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libx11-xcb1 \
    libgdk-pixbuf2.0-0 \
    libdbus-glib-1-2 \
    libnspr4 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libxdamage1 \
    libxfixes3 \
    libxxf86vm1 \
    && rm -rf /var/lib/apt/lists/*

# Chrome
RUN wget https://storage.googleapis.com/chrome-for-testing-public/140.0.7339.207/linux64/chrome-linux64.zip \
    && unzip chrome-linux64.zip -d /opt \
    && rm chrome-linux64.zip \
    && mkdir -p /opt/google \
    && mv /opt/chrome-linux64 /opt/google/chrome

# ChromeDriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/140.0.7339.207/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip -d /usr/local/bin \
    && rm chromedriver-linux64.zip \
    && mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

USER airflow

# Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt psycopg2-binary
