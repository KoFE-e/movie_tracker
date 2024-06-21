FROM python:3.12
EXPOSE 8000
WORKDIR /app
COPY . /app
RUN chmod +x *.sh
RUN pip3 install -r requirements.txt --no-cache-dir