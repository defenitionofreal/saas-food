FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /efood
COPY requirements.txt /efood/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /efood
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]