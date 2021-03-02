FROM python:3.8-slim

RUN pip install requests aiogram gunicorn httpx pydantic motor pymongo

COPY . .

EXPOSE 7040

CMD ["python", "src/core/application.py"]