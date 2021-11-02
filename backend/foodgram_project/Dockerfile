FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
# RUN pip3 install -r requirements.txt
RUN pip install -r /code/requirements.txt
COPY . .
CMD gunicorn foodgram_project.wsgi:application --bind 0:8000
# CMD python /code/manage.py runserver 0:8000 