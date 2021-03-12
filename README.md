# Manager Telegram Bot (ClickUp, Hubstaff, Развлечения)

### Бот предназначен для автоматизации рабочих процессов разработчикам и менеджерам.

[![Watch the video](https://telemetr.me/photos/9ba494205fe9a008f9e69ba373f77a3f.jpg)](https://filebin.net/wx73rqrhxrziozup/______________2021-03-12_17_07_54.mp4?t=ao3prpho)

## Интегрирование бота
### Создание бота в телеграмм 
Для начала создайте бота в телеграмм через @BotFather
1) /newbot
2) Имя бота
3) Скопируйте значения токена из ответа "Use this token to access the HTTP API:
1642*****:AAFZ5***********"

### Подключение приложения в ClickUp
Инструкция по подключению: https://github.com/AlexDemure/clickup_api

### Подключение приложения в Hubstaff
Инструкция по подключению: https://github.com/AlexDemure/hubstaff_api

### Развертывание бота
На этом этапе у вас на руках должно быть:
- Телеграм токен
- ClickUp Public key & Secret key
- HubStaff Public key & Secret key
- Личный сервер с доменом (VPS, Domain) (Для локальной разработки используйте ngrok)

#### Технологии 
- Python (Aiogram, aiohttp, gunicor, httpx)
- MongoDB
- Docker & Docker-compose

#### Требуемые зависимости до развертывания
- Docker
- Docker-compose


Клонирование репозитория
```
git clone https://github.com/AlexDemure/telegram
cd telegram
```
Заполнение конфигурационных данных системы
```
cd telegram
cp .env.example .env

>>> touch .env

ENV=PROD

# Стандартные значения для нашей БД
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=rootpassword
MONGO_HOST=localhost
MONGO_PORT=27017

TELEGRAM_API_TOKEN=*****:*****

CLICKUP_CLIENT_ID=Q1KVAP3M2Q8S6HULJ*******
CLICKUP_SECRET_KEY=P1U2N2AN0FNV7CUO********

HUBSTAFF_CLIENT_ID=1PZ9zOi5sZNE6-******************
HUBSTAFF_SECRET_KEY=RSwPUs8i2vsrxodnI-xEycxFbN-*********

WEBHOOK_HOST=https://example.com  # ваш домен или ngrok хост
```
Запуск процесса сборки
```
docker-compose up -d --build
```
Просмотр логов
```
docker logs -f telegram

DEBUG:aiogram.Middleware:Loaded middleware 'LoggingMiddleware'
[2021-03-12 11:53:44 +0000] [8] [INFO] Starting gunicorn 20.0.4
[2021-03-12 11:53:44 +0000] [8] [INFO] Listening at: http://127.0.0.1:7040 (8)
[2021-03-12 11:53:44 +0000] [8] [INFO] Using worker: aiohttp.GunicornWebWorker
[2021-03-12 11:53:44 +0000] [10] [INFO] Booting worker with pid: 10
DEBUG:aiogram.Middleware:Loaded middleware 'LoggingMiddleware'
DEBUG:aiogram:Make request: "getWebhookInfo" with data: "{}" and files "None"
DEBUG:aiogram:Response for getWebhookInfo: [200] "'{"ok":true,"result":{"url":"https://4f1e235627e0.ngrok.io/webhook","has_custom_certificate":false,"pending_update_count":0,"max_connections":40,"ip_address":"3.134.125.175"}}'"
INFO:root:Webhook data: {"url": "https://4f1e235627e0.ngrok.io/webhook", "has_custom_certificate": false, "pending_update_count": 0, "max_connections": 40, "ip_address": "3.134.125.175"}
INFO:apscheduler.scheduler:Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO:apscheduler.scheduler:Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO:apscheduler.scheduler:Adding job tentatively -- it will be properly scheduled when the scheduler starts
INFO:apscheduler.scheduler:Added job "daily_send_list_tasks" to job store "default"
INFO:apscheduler.scheduler:Added job "daily_send_list_tasks_with_unset_time" to job store "default"
INFO:apscheduler.scheduler:Added job "daily_send_today_time_tracked_and_activity" to job store "default"
INFO:apscheduler.scheduler:Scheduler started
DEBUG:aiogram:Make request: "deleteWebhook" with data: "{}" and files "None"
DEBUG:apscheduler.scheduler:Looking for jobs to run
DEBUG:apscheduler.scheduler:Next wakeup is due at 2021-03-12 22:00:00+03:00 (in 25574.787675 seconds)
```
### Подключение MongoDB локально
Инструкция по подключению: https://github.com/AlexDemure/fastapi_mongo