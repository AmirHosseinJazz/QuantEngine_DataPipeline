FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y wget gnupg unzip fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libcurl4 libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libu2f-udev libvulkan1 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y netcat-traditional \
    && pip install --no-cache-dir psycopg2-binary \
    && pip install -U prefect


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
    
    

# ENV PYTHON_TA_LIB_VERSION 0.4.17

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*


# RUN apt-get update && apt-get install -y gcc wget python3-dev musl-dev g++ make cmake autoconf ninja-build vim


# RUN pip3 install --upgrade pip
# RUN pip3 install setuptools numpy patchelf


# RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
#     tar -xvzf ta-lib-0.4.0-src.tar.gz && \
#     cd ta-lib/ && \
#     ./configure --prefix=/usr && \
#     make && \
#     make install


# ENV TA_LIBRARY_PATH="/usr/lib"
# ENV TA_INCLUDE_PATH="/usr/include"

# RUN pip3 install --global-option=build_ext --global-option="-L/usr/lib" TA-Lib
# RUN pip3 install -r requirements.txt

# ENV PATH="/usr/bin:$PATH"
# ENV LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"
# ENV PKG_CONFIG_PATH="/usr/lib/pkgconfig:$PKG_CONFIG_PATH"
    # copy

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
    
    
COPY . /app

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
