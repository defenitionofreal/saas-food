FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /efood_backend

WORKDIR /efood_backend

COPY requirements.txt /efood_backend/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /efood_backend/
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]