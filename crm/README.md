# CRM GraphQL System - Setup & Configuration Guide

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Prerequisites](#-prerequisites)
- [Quick Installation](#-quick-installation)
- [Database Setup](#-database-setup)
- [Environment Configuration](#-environment-configuration)
- [Service Configuration](#-service-configuration)
- [Testing & Verification](#-testing--verification)
- [Troubleshooting](#-troubleshooting)
- [Production Deployment](#-production-deployment)

## 🎯 Project Overview

A comprehensive CRM system with GraphQL API featuring:
- Automated customer management
- Order tracking with reminders  
- Real-time stock alerts
- Scheduled reporting
- Health monitoring

## 🛠 Prerequisites

### System Requirements
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Virtual Environment

### Package Installation
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
  redis-server postgresql postgresql-contrib

# macOS
brew install python3 redis postgresql

# Windows (WSL recommended)
# Install Python 3.11+ from python.org
# Install Redis from https://github.com/microsoftarchive/redis/releases
# Install PostgreSQL from https://www.postgresql.org/download/windows/
```

## 🚀 Quick Installation

### 1. Clone & Setup
```bash
# Clone repository
git clone <repository-url>
cd alx-backend-graphql_crm

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Start PostgreSQL
# Ubuntu/Debian:
sudo service postgresql start
# macOS:
brew services start postgresql

# Create database
sudo -u postgres psql << EOF
CREATE DATABASE crm_graphql;
CREATE USER crm_user WITH PASSWORD 'crm_password';
ALTER ROLE crm_user SET client_encoding TO 'utf8';
ALTER ROLE crm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crm_graphql TO crm_user;
EOF
```

### 3. Environment Configuration
Create `.env` file in project root:

```bash
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=crm_graphql
DB_USER=crm_user
DB_PASSWORD=crm_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
TIME_ZONE=UTC

# Redis/Celery Settings
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CRM Settings
INACTIVE_CUSTOMER_DAYS=365
ORDER_REMINDER_DAYS=7
LOW_STOCK_THRESHOLD=10
STOCK_RESTOCK_AMOUNT=10

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4. Apply Migrations
```bash
python manage.py migrate
python manage.py createsuperuser  # Optional: Create admin account
```

## ⚙️ Service Configuration

### 1. Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Django
python manage.py runserver

# Terminal 3: Start Celery Worker
celery -A crm worker -l info --concurrency=4

# Terminal 4: Start Celery Beat
celery -A crm beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Terminal 5: Start Flower (optional monitoring)
celery -A crm flower --port=5555
```

### 2. Configure Crontab
```bash
# Add cron jobs
python manage.py crontab add

# Verify cron jobs
python manage.py crontab show

# Expected output:
# (hash_id) -> ('*/5 * * * *', 'crm.cron.log_crm_heartbeat')
# (hash_id) -> ('0 */12 * * *', 'crm.cron.update_low_stock')
```

## 🔍 Testing & Verification

### 1. Basic System Check
```bash
# Verify GraphQL endpoint
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { hello }"}'

# Verify Redis
redis-cli ping  # Should return "PONG"

# Verify PostgreSQL
pg_isready -h localhost -p 5432
```

### 2. Manual Task Testing
```python
# In Django shell
python manage.py shell

>>> from crm.cron import log_crm_heartbeat, update_low_stock
>>> log_crm_heartbeat()  # Check /tmp/crm_heartbeat_log.txt
>>> update_low_stock()   # Check /tmp/low_stock_updates_log.txt

>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report.delay()
>>> result.get(timeout=30)  # Check /tmp/crm_report_log.txt
```

### 3. Scheduled Tasks Verification
| Task | Schedule | Log File | Description |
|------|----------|----------|-------------|
| Heartbeat Logger | Every 5 minutes | `/tmp/crm_heartbeat_log.txt` | System health check |
| Customer Cleanup | Sunday 2:00 AM | `/tmp/customer_cleanup_log.txt` | Remove inactive customers |
| Order Reminders | Daily 8:00 AM | `/tmp/order_reminders_log.txt` | Send order alerts |
| Stock Updates | Every 12 hours | `/tmp/low_stock_updates_log.txt` | Restock low inventory |
| CRM Reports | Monday 6:00 AM | `/tmp/crm_report_log.txt` | Generate weekly reports |

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```bash
# Check PostgreSQL status
sudo service postgresql status

# Test connection
python manage.py dbshell

# Reset if needed
sudo -u postgres psql -c "DROP DATABASE crm_graphql;"
sudo -u postgres psql -c "CREATE DATABASE crm_graphql;"
python manage.py migrate
```

#### 2. Redis Not Working
```bash
# Check Redis status
redis-cli ping

# Restart Redis
sudo systemctl restart redis-server

# Clear cache
redis-cli flushall
```

#### 3. Cron Jobs Not Executing
```bash
# Check cron service
sudo service cron status

# Restart cron
sudo service cron restart

# Check logs
sudo tail -f /var/log/syslog | grep CRON

# Test specific cron job
python manage.py crontab run [job-hash]
```

#### 4. Celery Issues
```bash
# Restart Celery worker
pkill -9 -f "celery worker"
celery -A crm worker -l info --concurrency=4

# Purge task queue
celery -A crm purge

# Check active tasks
celery -A crm inspect active
```

#### 5. Permission Problems
```bash
# Fix log file permissions
chmod 666 /tmp/*_log.txt 2>/dev/null || true
chown $USER:$USER /tmp/*_log.txt 2>/dev/null || true

# Make scripts executable
chmod +x crm/cron_jobs/*.sh
chmod +x crm/cron_jobs/*.py
```

#### 6. GraphQL Endpoint Issues
```bash
# Check Django server
curl http://localhost:8000/graphql

# Check port conflicts
lsof -i :8000

# Run with verbose logging
python manage.py runserver --verbosity 3
```

## 📊 Health Monitoring

### Health Check Script
Create `check_services.sh`:

```bash
#!/bin/bash
echo "=== CRM System Health Check ==="
echo "Time: $(date)"
echo ""

# Check Django
curl -s http://localhost:8000/graphql > /dev/null && \
  echo "✓ Django Server: RUNNING" || echo "✗ Django Server: DOWN"

# Check PostgreSQL
pg_isready -h localhost -p 5432 > /dev/null && \
  echo "✓ PostgreSQL: RUNNING" || echo "✗ PostgreSQL: DOWN"

# Check Redis
redis-cli ping 2>/dev/null | grep -q PONG && \
  echo "✓ Redis: RUNNING" || echo "✗ Redis: DOWN"

# Check Celery
ps aux | grep -q "[c]elery worker" && \
  echo "✓ Celery Worker: RUNNING" || echo "✗ Celery Worker: DOWN"

echo ""
echo "=== Recent Heartbeats ==="
tail -3 /tmp/crm_heartbeat_log.txt 2>/dev/null || echo "No heartbeat logs"
```

```bash
chmod +x check_services.sh
./check_services.sh
```

### Log File Locations
```
Application Logs:
- Django: logs/django.log
- GraphQL: logs/graphql.log
- Cron Jobs: logs/cron.log
- Celery: logs/celery.log

Task Outputs:
- Heartbeat: /tmp/crm_heartbeat_log.txt
- Customer Cleanup: /tmp/customer_cleanup_log.txt
- Order Reminders: /tmp/order_reminders_log.txt
- Stock Updates: /tmp/low_stock_updates_log.txt
- Reports: /tmp/crm_report_log.txt
```

## 🚀 Production Deployment

### 1. Production Configuration
Update `.env` for production:

```bash
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<generate-secure-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/dbname
REDIS_URL=redis://:password@host:port/db
```

### 2. Using Gunicorn & Supervisor
```bash
# Install Gunicorn
pip install gunicorn

# Supervisor configuration (/etc/supervisor/conf.d/crm.conf)
[program:crm_gunicorn]
command=/path/to/venv/bin/gunicorn crm.wsgi:application --bind 0.0.0.0:8000
directory=/path/to/alx-backend-graphql_crm
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/crm/gunicorn.err.log
stdout_logfile=/var/log/crm/gunicorn.out.log

[program:crm_celery]
command=/path/to/venv/bin/celery -A crm worker -l info
directory=/path/to/alx-backend-graphql_crm
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/crm/celery.err.log
stdout_logfile=/var/log/crm/celery.out.log
```

### 3. Nginx Configuration
```nginx
# /etc/nginx/sites-available/crm
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/alx-backend-graphql_crm/staticfiles/;
    }

    location /media/ {
        alias /path/to/alx-backend-graphql_crm/media/;
    }
}
```

## 📚 Quick Reference

### Start All Services
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Django
python manage.py runserver

# Terminal 3: Celery Worker
celery -A crm worker -l info

# Terminal 4: Celery Beat
celery -A crm beat -l info

# Terminal 5: Monitoring (optional)
celery -A crm flower --port=5555
```

### Reset System
```bash
# Clear all data and restart
redis-cli flushall
python manage.py flush --noinput
python manage.py migrate
python manage.py crontab remove
python manage.py crontab add
```

### View Logs
```bash
# Real-time log monitoring
tail -f /tmp/crm_heartbeat_log.txt
tail -f logs/django.log
tail -f logs/celery.log
```

## ❓ Getting Help

If you encounter issues:
1. Check the relevant log file
2. Verify all services are running
3. Review the troubleshooting section
4. Check file permissions
5. Ensure environment variables are set

For additional support, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [GraphQL Documentation](https://graphql.org/learn/)
