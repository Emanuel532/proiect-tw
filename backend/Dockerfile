FROM python:3.8

WORKDIR /backend
COPY skillshare_backend /backend/
RUN apt-get update && apt-get install -y default-libmysqlclient-dev && pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]