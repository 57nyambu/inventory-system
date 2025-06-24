Inventory Management System (Kenyan Market) - Technical Implementation Guide
Python/Django Backend with Realtime Analytics, M-Pesa, and SMS Integration

1. System Overview
A Django-based inventory management system with:

Multi-warehouse stock tracking

M-Pesa payments (Daraja API)

AfricasTalking SMS for receipts/alerts

Realtime analytics dashboards (WebSockets)

Role-based access control (Admin, Procurement, Cashiers)

2. Prerequisites
Python 3.9+

PostgreSQL (Recommended) / SQLite (Development)

Redis (For Celery & WebSockets)

Safaricom Developer Account (Daraja API)

AfricasTalking Account (SMS API)

3. Project Setup
3.1. Clone & Install Dependencies
bash
git clone https://github.com/your-repo/inventory-system.git
cd inventory-system
python -m venv venv
source venv/bin/activate  # Linux/Mac | venv\Scripts\activate (Windows)
pip install -r requirements.txt
3.2. Key Django Apps Structure
text
apps/
├── accounts/          # User auth, roles (formerly 'users')
├── analytics/         # Realtime dashboards, reports
├── core/              # Base models, utils
├── integrations/      # M-Pesa, SMS APIs
├── products/          # SKUs, categories, inventory
├── procurement/       # Purchase orders, suppliers
├── sales/             # POS, orders, receipts
├── warehouses/        # Locations, bins, transfers
3.3. Environment Variables (.env)
ini
# Database
DB_NAME=inventory
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost

# M-Pesa (Daraja)
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/mpesa-callback/

# AfricasTalking SMS
AT_USERNAME=sandbox
AT_API_KEY=your_api_key
AT_SENDER_ID=INVENT

# Celery & Redis
REDIS_URL=redis://localhost:6379/0
3.4. Django Settings (settings.py)
python
# Core Settings
INSTALLED_APPS = [
    'apps.accounts',
    'apps.analytics',
    'apps.core',
    'apps.integrations',
    'apps.products',
    'apps.procurement',
    'apps.sales',
    'apps.warehouses',
    'channels',  # For WebSockets
]

# Auth
AUTH_USER_MODEL = 'accounts.User'

# Realtime
ASGI_APPLICATION = 'config.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('localhost', 6379)]},
    },
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Africa/Nairobi'
4. Database Setup
4.1. Migrations
bash
python manage.py makemigrations
python manage.py migrate
4.2. Create Superuser
bash
python manage.py createsuperuser
5. Key Implementations
5.1. M-Pesa Integration
File: apps/integrations/mpesa.py
python
# (Refer to previous M-Pesa gateway implementation)
Test M-Pesa Sandbox
bash
curl -X POST https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "BusinessShortCode": "174379",
    "Password": "YOUR_ENCODED_PASS",
    "Timestamp": "20230831120000",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": "100",
    "PartyA": "254708374149",
    "PartyB": "174379",
    "PhoneNumber": "254708374149",
    "CallBackURL": "https://yourdomain.com/mpesa-callback/",
    "AccountReference": "ORDER_1",
    "TransactionDesc": "Test"
  }'
5.2. Realtime Analytics
Start WebSocket Server
bash
daphne config.asgi:application --port 8000
Frontend JS (WebSocket Client)
javascript
const socket = new WebSocket('ws://localhost:8000/ws/analytics/sales/');
socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log("New sale:", data.total);
};
5.3. SMS Receipts
Test AfricasTalking SMS
python
from integrations.sms import SMSService
SMSService().send_receipt("254712345678", "Test receipt")
6. Deployment
6.1. Production Stack
Web Server: Nginx + Gunicorn

ASGI: Daphne

Task Queue: Celery + Redis

Database: PostgreSQL

6.2. Sample Nginx Config
nginx
server {
    listen 80;
    server_name inventory.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /ws/ {
        proxy_pass http://localhost:8001;  # Daphne port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
6.3. Supervisor Config
ini
[program:celery]
command=celery -A config worker --loglevel=info
directory=/path/to/project
user=www-data
autostart=true
autorestart=true

[program:daphne]
command=daphne -p 8001 config.asgi:application
directory=/path/to/project
user=www-data
autostart=true
7. Testing
7.1. Automated Tests
bash
python manage.py test apps.accounts apps.sales
7.2. Postman Collection
Download Postman Collection

Includes:

M-Pesa STK Push

SMS API

WebSocket endpoints

8. Support & Troubleshooting
Issue	Solution
M-Pesa callback fails	Ensure HTTPS + valid SSL cert
SMS not delivered	Check AfricasTalking balance/Sender ID
WebSocket disconnect	Verify Redis server is running
9. License
MIT License. See LICENSE.

