FROM python:3.9

# Postavi radni direktorijum
WORKDIR /app

# Kopiraj requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopiraj ostatak aplikacije
COPY . .

# Izloži port na kojem Django aplikacija radi
EXPOSE 8000

# Pokreni Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
