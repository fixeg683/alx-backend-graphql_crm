# 🚀 CRM GraphQL System - Complete Setup & Operations Guide

## 📋 Table of Contents

1. [System Requirements](#-system-requirements)
2. [Quick Start Installation](#-quick-start-installation-5-minutes)
3. [Detailed Setup Guide](#-detailed-setup-guide)
4. [Service Configuration](#-service-configuration)
5. [Testing & Verification](#-testing--verification)
6. [Cron Jobs & Scheduled Tasks](#-cron-jobs--scheduled-tasks)
7. [Troubleshooting](#-troubleshooting)
8. [Production Deployment](#-production-deployment)
9. [API Reference](#-api-reference)

## 🎯 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **Redis**: 6.0 or higher
- **Operating System**: Linux, macOS, or Windows (WSL2 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free space

### Verify System Requirements
```bash
# Check Python version
python3 --version

# Check PostgreSQL version
psql --version

# Check Redis version
redis-server --version

# Check pip version
pip3 --version
```

## ⚡ Quick Start Installation (5 Minutes)

### Step 1: Clone Repository
```bash
# Clone the project
git clone <repository-url>
cd alx-backend-graphql_crm
```

### Step 2: Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Database Setup
```bash
# Start PostgreSQL
sudo service postgresql start  # Ubuntu/Debian
# or
brew services start postgresql  # macOS

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE crm_graphql;"
sudo -u postgres psql -c "CREATE USER crm_user WITH PASSWORD 'crm_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE crm_graphql TO crm_user;"
```

### Step 4: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file (update with your values)
nano .env
```

### Step 5: Initialize Project
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 6: Start Services
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Django
python manage.py runserver

# Terminal 3: Celery Worker
celery -A crm worker -l info

# Terminal 4: Celery Beat
celery -A crm beat -l info

# Terminal 5: Add cron jobs
python manage.py crontab add
```

## 🔧 Detailed Setup Guide

### 1. Operating System Specific Setup

**Ubuntu 20.04/22.04:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and build tools
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libpq-dev libssl-dev libffi-dev

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Redis
sudo apt install -y redis-server

# Install additional tools
sudo apt install -y curl git nano htop
```

**macOS (Homebrew):**
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install packages
brew install python3
brew install postgresql
brew install redis
brew install git

# Start services
brew services start postgresql
brew services start redis
```

**Windows (WSL2 Recommended):**
```powershell
# Enable WSL2 and install Ubuntu from Microsoft Store
# Then follow Ubuntu instructions above
```

### 2. Project Structure Setup
```bash
# Clone repository
git clone https://github.com/your-org/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install development packages (optional)
pip install black flake8 isort pre-commit
```

### 3. Database Configuration

**PostgreSQL Setup:**
```bash
# Access PostgreSQL
sudo -u postgres psql

# Execute these commands in PostgreSQL shell:
CREATE DATABASE crm_graphql;
CREATE USER crm_user WITH PASSWORD 'your_secure_password';
ALTER ROLE crm_user SET client_encoding TO 'utf8';
ALTER ROLE crm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crm_graphql TO crm_user;
\q

# Test connection
psql -h localhost -U crm_user -d crm_graphql -W
```

**Redis Setup:**
```bash
# Configure Redis (Linux)
sudo nano /etc/redis/redis.conf

# Update these settings:
# maxmemory 256mb
# maxmemory-policy allkeys-lru
# save 900 1
# save 300 10
# save 60 10000

# Restart Redis
sudo systemctl restart redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping
```

### 4. Environment Configuration

Create `.env` file in project root:

```bash
# ====================
# DJANGO SETTINGS
# ====================
SECRET_KEY='django-insecure-@w#d!$qk&nz7s5v8y9b0e1f2g3h4i5j6k7l8m9n0'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE='UTC'

# ====================
# DATABASE
# ====================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=crm_graphql
DB_USER=crm_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# ====================
# REDIS & CELERY
# ====================
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_TIMEZONE=UTC

# ====================
# CRM APPLICATION
# ====================
INACTIVE_CUSTOMER_DAYS=365
ORDER_REMINDER_DAYS=7
LOW_STOCK_THRESHOLD=10
STOCK_RESTOCK_AMOUNT=10
HEARTBEAT_INTERVAL_MINUTES=5

# ====================
# EMAIL (for notifications)
# ====================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# For production, use:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your_email@gmail.com
# EMAIL_HOST_PASSWORD=your_app_password

# ====================
# CORS & SECURITY
# ====================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Project Initialization

```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (follow prompts)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create necessary directories
mkdir -p logs media static
mkdir -p /tmp/crm_logs

# Set permissions
chmod 755 logs media static
chmod 755 /tmp/crm_logs
```

## 🚦 Service Configuration

### 1. Running All Services

**Using start script:**
```bash
# Create start script
cat > start_crm.sh << 'EOF'
#!/bin/bash
echo "Starting CRM System..."

# Start Redis
redis-server &
sleep 2

# Start Celery Worker
celery -A crm worker -l info --concurrency=4 &
sleep 2

# Start Celery Beat
celery -A crm beat -l info &
sleep 2

# Configure cron jobs
python manage.py crontab add

# Start Django
python manage.py runserver

echo "CRM System started successfully!"
EOF

chmod +x start_crm.sh
./start_crm.sh
```

**Manual Start (5 Terminals):**

| Terminal | Command | Purpose |
|----------|---------|---------|
| Terminal 1 | `redis-server` | Redis cache |
| Terminal 2 | `python manage.py runserver` | Django server |
| Terminal 3 | `celery -A crm worker -l info` | Task worker |
| Terminal 4 | `celery -A crm beat -l info` | Task scheduler |
| Terminal 5 | `python manage.py crontab add` | Cron jobs |

### 2. Crontab Configuration

```bash
# Add cron jobs to system
python manage.py crontab add

# Verify cron jobs
python manage.py crontab show

# Expected output:
# Currently active jobs in crontab:
# a1b2c3d4e5f6g7h8i9j0 -> ('*/5 * * * *', 'crm.cron.log_crm_heartbeat')
# b2c3d4e5f6g7h8i9j0a1 -> ('0 */12 * * *', 'crm.cron.update_low_stock')
# c3d4e5f6g7h8i9j0a1b2 -> ('0 2 * * 0', 'crm.cron.clean_inactive_customers')
# d4e5f6g7h8i9j0a1b2c3 -> ('0 8 * * *', 'crm.cron.send_order_reminders')

# Remove cron jobs
python manage.py crontab remove
```

### 3. Verify All Services

```bash
# Create verification script
cat > verify_services.sh << 'EOF'
#!/bin/bash
echo "=== CRM System Status Check ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "----------------------------------------"

# Check PostgreSQL
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL: RUNNING"
else
    echo "❌ PostgreSQL: NOT RUNNING"
fi

# Check Redis
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: RUNNING"
else
    echo "❌ Redis: NOT RUNNING"
fi

# Check Django
if curl -s http://localhost:8000/graphql > /dev/null; then
    echo "✅ Django Server: RUNNING"
else
    echo "❌ Django Server: NOT RUNNING"
fi

# Check Celery Worker
if ps aux | grep -q "[c]elery worker"; then
    echo "✅ Celery Worker: RUNNING"
else
    echo "❌ Celery Worker: NOT RUNNING"
fi

# Check Celery Beat
if ps aux | grep -q "[c]elery beat"; then
    echo "✅ Celery Beat: RUNNING"
else
    echo "❌ Celery Beat: NOT RUNNING"
fi

# Check Cron Jobs
if python manage.py crontab show > /dev/null 2>&1; then
    echo "✅ Cron Jobs: CONFIGURED"
    echo "   Active jobs:"
    python manage.py crontab show | sed 's/^/     /'
else
    echo "❌ Cron Jobs: NOT CONFIGURED"
fi

echo "----------------------------------------"
echo "Check complete!"
EOF

chmod +x verify_services.sh
./verify_services.sh
```

## ✅ Testing & Verification

### 1. GraphQL API Testing

```bash
# Test basic GraphQL endpoint
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { hello }"}' \
  && echo -e "\n✅ GraphQL API is working"

# Expected response: {"data": {"hello": "Hello from GraphQL!"}}

# Test with GraphQL query file
cat > test_query.gql << 'EOF'
query {
  hello
  totalCustomers
  totalOrders
}
EOF

curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { hello totalCustomers totalOrders }"}' \
  && echo -e "\n✅ Extended query successful"
```

### 2. Manual Task Execution

```bash
# Test cron jobs manually
python manage.py shell << 'EOF'
from datetime import datetime
from crm.cron import log_crm_heartbeat, update_low_stock
from crm.tasks import generate_crm_report

print("Testing CRM Tasks...")
print("=" * 40)

# Test 1: Heartbeat
print(f"{datetime.now()} - Testing heartbeat...")
try:
    log_crm_heartbeat()
    print("✅ Heartbeat logged successfully")
except Exception as e:
    print(f"❌ Heartbeat failed: {e}")

# Test 2: Stock Update
print(f"\n{datetime.now()} - Testing stock update...")
try:
    update_low_stock()
    print("✅ Stock update completed")
except Exception as e:
    print(f"❌ Stock update failed: {e}")

# Test 3: Report Generation
print(f"\n{datetime.now()} - Testing report generation...")
try:
    result = generate_crm_report.delay()
    print(f"✅ Report task submitted with ID: {result.id}")
    # Wait for result (timeout after 10 seconds)
    report = result.get(timeout=10)
    print(f"✅ Report result: {report}")
except Exception as e:
    print(f"❌ Report generation failed: {e}")

print("\n" + "=" * 40)
print("Manual task testing complete!")
EOF
```

### 3. Log File Verification

```bash
# Check log files are being created
echo "Checking log files..."
echo "======================"

LOGS=(
    "/tmp/crm_heartbeat_log.txt"
    "/tmp/customer_cleanup_log.txt"
    "/tmp/order_reminders_log.txt"
    "/tmp/low_stock_updates_log.txt"
    "/tmp/crm_report_log.txt"
    "logs/django.log"
    "logs/graphql.log"
    "logs/celery.log"
)

for log_file in "${LOGS[@]}"; do
    if [ -f "$log_file" ]; then
        size=$(wc -l < "$log_file" 2>/dev/null || echo "0")
        echo "✅ $log_file: Exists ($size lines)"
    else
        echo "⚠️  $log_file: Not found (will be created automatically)"
    fi
done

# View recent heartbeat logs
echo -e "\nRecent Heartbeat Logs:"
echo "========================"
tail -5 /tmp/crm_heartbeat_log.txt 2>/dev/null || echo "No heartbeat logs yet"
```

### 4. Web Interface Verification

| Interface | URL | Default Credentials | Purpose |
|-----------|-----|---------------------|---------|
| GraphQL Playground | http://localhost:8000/graphql | None | Interactive API testing |
| Django Admin | http://localhost:8000/admin | Created during setup | System administration |
| Flower Monitor | http://localhost:5555 | None (optional) | Celery task monitoring |

**Test Admin Access:**
```bash
# Create admin if not exists
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created: admin / admin123")
else:
    print("Admin user already exists")
EOF

# Test admin login
curl -s http://localhost:8000/admin/login/ | grep csrfmiddlewaretoken \
  && echo "✅ Admin interface is accessible"
```

## 📅 Cron Jobs & Scheduled Tasks

### Scheduled Tasks Overview

| Task | Schedule | Description | Log File |
|------|----------|-------------|----------|
| Heartbeat Logger | Every 5 minutes | System health monitoring | `/tmp/crm_heartbeat_log.txt` |
| Customer Cleanup | Sunday 2:00 AM | Remove inactive customers | `/tmp/customer_cleanup_log.txt` |
| Order Reminders | Daily 8:00 AM | Send pending order alerts | `/tmp/order_reminders_log.txt` |
| Stock Updates | Every 12 hours | Restock low inventory | `/tmp/low_stock_updates_log.txt` |
| CRM Reports | Monday 6:00 AM | Weekly business report | `/tmp/crm_report_log.txt` |

### Manual Cron Job Testing

```bash
# Test each cron job manually
python manage.py shell << 'EOF'
import subprocess
from datetime import datetime

jobs = {
    "heartbeat": "crm.cron.log_crm_heartbeat",
    "stock_update": "crm.cron.update_low_stock",
    "customer_cleanup": "crm.cron.clean_inactive_customers",
    "order_reminders": "crm.cron.send_order_reminders"
}

for name, module in jobs.items():
    print(f"\nTesting {name}...")
    try:
        # Import and execute
        exec(f"from {module} import {module.split('.')[-1]}")
        exec(f"{module.split('.')[-1]}()")
        print(f"✅ {name}: Success")
    except Exception as e:
        print(f"❌ {name}: Failed - {str(e)}")
EOF
```

### View Cron Job Logs

```bash
# System cron logs
sudo tail -f /var/log/syslog | grep CRON

# Application cron logs
tail -f /tmp/crm_heartbeat_log.txt

# Check cron job status
python manage.py crontab show --format=json
```

## 🔧 Troubleshooting

### Common Issues & Solutions

**Issue 1: "Port already in use"**
```bash
# Check which process is using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

**Issue 2: Database connection failed**
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Test database connection
python manage.py dbshell

# Reset database (if needed)
sudo -u postgres psql -c "DROP DATABASE IF EXISTS crm_graphql;"
sudo -u postgres psql -c "CREATE DATABASE crm_graphql;"
python manage.py migrate
```

**Issue 3: Redis connection error**
```bash
# Check Redis service
redis-cli ping

# Restart Redis
sudo systemctl restart redis-server

# Check Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

**Issue 4: Celery worker not starting**
```bash
# Stop all Celery processes
pkill -9 -f "celery worker"
pkill -9 -f "celery beat"

# Start fresh
celery -A crm worker -l info --concurrency=4
celery -A crm beat -l info
```

**Issue 5: Permission denied for log files**
```bash
# Fix permissions
sudo chown -R $USER:$USER /tmp/crm_*_log.txt
sudo chmod 664 /tmp/crm_*_log.txt

# Create log directory
mkdir -p /tmp/crm_logs
chmod 777 /tmp/crm_logs
```

**Issue 6: Module import errors**
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify Django setup
python manage.py check
```

### Diagnostic Commands

```bash
# Run complete diagnostic
cat > diagnose.sh << 'EOF'
#!/bin/bash
echo "=== CRM System Diagnostic ==="
date
echo ""

echo "1. Python Environment:"
echo "   Python: $(python3 --version 2>/dev/null || echo 'Not found')"
echo "   Pip: $(pip3 --version 2>/dev/null || echo 'Not found')"
echo "   Virtual Environment: $(which python3 | grep venv && echo 'Active' || echo 'Not active')"
echo ""

echo "2. Database Status:"
if command -v pg_isready &> /dev/null; then
    pg_isready -h localhost -p 5432 && echo "   PostgreSQL: ✅ Accessible" || echo "   PostgreSQL: ❌ Not accessible"
else
    echo "   PostgreSQL: ⚠️  pg_isready not found"
fi
echo ""

echo "3. Redis Status:"
if command -v redis-cli &> /dev/null; then
    redis-cli ping 2>/dev/null && echo "   Redis: ✅ Running" || echo "   Redis: ❌ Not running"
else
    echo "   Redis: ⚠️  redis-cli not found"
fi
echo ""

echo "4. Django Status:"
if [ -f "manage.py" ]; then
    python manage.py check --deploy 2>/dev/null | head -5
else
    echo "   ⚠️  manage.py not found in current directory"
fi
echo ""

echo "5. Service Status:"
echo "   Django Server: $(ps aux | grep -c '[r]unserver') instances"
echo "   Celery Worker: $(ps aux | grep -c '[c]elery worker') instances"
echo "   Celery Beat: $(ps aux | grep -c '[c]elery beat') instances"
echo ""

echo "6. Disk Usage:"
df -h . | tail -1
echo ""

echo "Diagnostic complete!"
EOF

chmod +x diagnose.sh
./diagnose.sh
```

## 🚀 Production Deployment

### Production Environment Setup

**Update `.env` for production:**
```bash
# Security
DEBUG=False
SECRET_KEY='generate-new-secure-key-here'
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,server_ip

# Database (use production database)
DB_NAME=production_crm
DB_USER=production_user
DB_PASSWORD='strong-production-password'

# Redis (with authentication if needed)
REDIS_URL=redis://:password@localhost:6379/0

# HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Production Service Management

**Using Systemd (Linux):**
```bash
# Create systemd service files
sudo nano /etc/systemd/system/crm.service
```

**crm.service:**
```ini
[Unit]
Description=CRM Django Application
After=network.target postgresql.service redis-server.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/alx-backend-graphql_crm
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/alx-backend-graphql_crm/.env
ExecStart=/path/to/venv/bin/gunicorn \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/crm/access.log \
  --error-logfile /var/log/crm/error.log \
  crm.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**celery.service:**
```ini
[Unit]
Description=CRM Celery Worker
After=network.target redis-server.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/alx-backend-graphql_crm
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/alx-backend-graphql_crm/.env
ExecStart=/path/to/venv/bin/celery -A crm worker -l info --concurrency=4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable services:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable crm.service
sudo systemctl enable celery.service
sudo systemctl start crm.service
sudo systemctl start celery.service
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/crm
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/alx-backend-graphql_crm/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/alx-backend-graphql_crm/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    location /graphql {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
}
```

## 📚 API Reference

### GraphQL Queries

**Basic Queries:**
```graphql
# System Health
query {
  hello
}

# Customer Statistics
query {
  totalCustomers
  activeCustomers
  inactiveCustomers
}

# Order Statistics
query {
  totalOrders
  recentOrders(limit: 10) {
    id
    totalAmount
    orderDate
    customer {
      name
      email
    }
  }
}

# Product Inventory
query {
  lowStockProducts(threshold: 10) {
    id
    name
    stock
    price
  }
}
```

### GraphQL Mutations

```graphql
# Update low stock products
mutation {
  updateLowStockProducts {
    message
    updatedCount
    products {
      id
      name
      stock
    }
  }
}

# Create new order
mutation {
  createOrder(input: {
    customerId: "1"
    products: [
      {productId: "1", quantity: 2},
      {productId: "2", quantity: 1}
    ]
  }) {
    order {
      id
      totalAmount
      orderDate
    }
    success
    message
  }
}
```

## 📞 Support & Maintenance

### Regular Maintenance Tasks

```bash
# Daily health check
./verify_services.sh

# Weekly backup
python manage.py dumpdata --indent 2 > backup_$(date +%Y%m%d).json

# Monthly log rotation
sudo logrotate /etc/logrotate.d/crm

# Quarterly security updates
pip list --outdated
pip install --upgrade -r requirements.txt
```

### Getting Help

1. **Check Logs**: `/tmp/crm_*_log.txt` and `logs/` directory
2. **Verify Services**: Run `./verify_services.sh`
3. **Check Environment**: Ensure `.env` file is properly configured
4. **Review Documentation**: Refer to this README
5. **Community Support**: Check project issues on GitHub

### Emergency Procedures

**System won't start:**
```bash
# Stop all services
pkill -9 -f "python"
pkill -9 -f "celery"
pkill -9 -f "redis-server"

# Clear cache
redis-cli flushall

# Start fresh
./start_crm.sh
```

**Database corruption:**
```bash
# Backup current data
python manage.py dumpdata --indent 2 > emergency_backup.json

# Reset database
sudo -u postgres psql -c "DROP DATABASE crm_graphql;"
sudo -u postgres psql -c "CREATE DATABASE crm_graphql;"
python manage.py migrate

# Restore data (if backup exists)
python manage.py loaddata emergency_backup.json
```

---

## ✅ Success Checklist

- [ ] All services running (Django, Redis, Celery, PostgreSQL)
- [ ] GraphQL API accessible at http://localhost:8000/graphql
- [ ] Cron jobs configured (`python manage.py crontab show`)
- [ ] Log files being created in `/tmp/`
- [ ] Database migrations applied
- [ ] Admin user created
- [ ] Environment variables set in `.env`
- [ ] Static files collected
- [ ] All tests passing

If all items are checked, your CRM GraphQL system is fully operational! 🎉

---

**Version**: 1.0.0  
**Last Updated**: $(date +%Y-%m-%d)  
**Support**: Check GitHub Issues for help  
**Documentation**: Always refer to the latest version of this guide
