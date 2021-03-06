FROM python:3.8-slim

RUN pip install requests aiogram gunicorn aiohttp httpx pydantic motor pymongo APScheduler tenacity

COPY . .

EXPOSE 7040

ENV PYTHONPATH=/

CMD ["python", "src/core/application.py"]