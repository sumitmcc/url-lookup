FROM python:latest
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app /app
COPY tests /app/tests
#WORKDIR /app
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=cisco.123
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306
ENV MYSQL_DB=malware
ENV FLASK_ENV=development
EXPOSE 5123
#CMD ["flask", "run"]
CMD ["gunicorn"  , "-c", "app/gunicorn_config.py", "app.wsgi:app"]