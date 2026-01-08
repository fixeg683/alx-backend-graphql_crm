# CRM GraphQL System Setup Guide

## Prerequisites

### 1. Install Redis
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# macOS
brew install redis
brew services start redis

# Verify Redis is running
redis-cli ping
