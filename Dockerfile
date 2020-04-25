FROM python:3.7
WORKDIR /app
COPY . .
RUN apt update && apt upgrade -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python server2.py