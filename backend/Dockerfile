FROM python:latest
WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# CMD [ "python3", "manage.py", "runserver", "0:8000"]
CMD ["gunicorn", "fg_back.wsgi:application" , "--bind" , "0:8000"]

