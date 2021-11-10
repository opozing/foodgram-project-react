FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN pip install -r /code/requirements.txt
COPY . .
CMD gunicorn foodgram_project.wsgi:application --bind 0:8000
