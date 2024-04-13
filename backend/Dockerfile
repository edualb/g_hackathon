FROM python:3.12.3

WORKDIR /app
COPY . .

RUN pip install -r /app/requirements.txt

EXPOSE 8000

ENTRYPOINT ["python3"]
CMD ["/app/main.py"]