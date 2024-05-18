FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y wget gnupg unzip fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libcurl4 libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libu2f-udev libvulkan1 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y netcat-traditional \
    && pip install --no-cache-dir psycopg2-binary \
    && pip install -U prefect

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Download and install Google Chrome
RUN apt-get update \
    && wget -q --continue -P /tmp "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" \
    && dpkg -i /tmp/google-chrome-stable_current_amd64.deb

# Set up environment variables
ENV CHROME_DRIVER_PATH /usr/local/bin/chromedriver

# Download and install Chromedriver
RUN wget -q -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/95.0.4638.54/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin \
    && chmod +x $CHROME_DRIVER_PATH \
    && rm /tmp/chromedriver_linux64.zip

    
    
# copy
COPY . /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
