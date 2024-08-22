# Koristi Python 3.9 kao osnovnu sliku
FROM python:3.9-slim

# Instaliraj zavisnosti
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instaliraj Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y && \
    rm google-chrome-stable_current_amd64.deb

# Instaliraj ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Postavi radni direktorijum
WORKDIR /app

# Kopiraj requirements.txt i instaliraj Python zavisnosti
COPY myproject/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiraj ostatak aplikacije
COPY myproject/ .

# Definiši komandnu liniju za pokretanje aplikacije
CMD ["python", "manage.py", "test"]
