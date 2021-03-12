FROM python:3.8-slim

RUN pip install requests aiogram gunicorn aiohttp httpx pydantic motor pymongo APScheduler tenacity google_trans_new

COPY . .

EXPOSE 7040

ENV PYTHONPATH=/

