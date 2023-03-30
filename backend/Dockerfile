FROM python:3.8.5
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram.wsgi:application" , "--bind" , "0:8000"]
