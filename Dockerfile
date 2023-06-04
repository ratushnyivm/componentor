FROM python:3.11.2

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/componentor/

COPY requirements.txt /usr/src

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/componentor/

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
