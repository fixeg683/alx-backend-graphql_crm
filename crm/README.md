# CRM GraphQL System - Complete Setup Guide

## 📋 Overview
This CRM system features a GraphQL API with automated scheduling via cron jobs and Celery tasks for customer management, order tracking, stock alerts, and reporting.

## 🚀 Quick Start

### 1. Prerequisites Installation

```bash
# Install system dependencies
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv redis-server postgresql postgresql-contrib

# macOS
brew install python3 redis postgresql

# Windows (using WSL or PowerShell)
# Install Python 3.11+ from python.org
# Install Redis from https://github.com/microsoftarchive/redis/releases
# Install PostgreSQL from https://www.postgresql.org/download/windows/
