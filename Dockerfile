FROM python:latest
COPY app /app
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=cisco.123
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306
ENV MYSQL_DB=malware
ENV FLASK_ENV=development
EXPOSE 5123
CMD ["flask", "run"]