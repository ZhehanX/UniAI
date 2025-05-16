# Project Setup Guide

This guide walks you through setting up and running the project using Docker.

## Prerequisites

- Ensure [Docker](https://www.docker.com/) is **installed and running** on your machine.

---

## Getting Started

Follow these steps from the **root directory** of the project:

### 1. Build Docker Images

```bash
docker-compose build
```
### 2. Start Docker Containers
```bash
docker-compose up
```
### 3. Restore the Database from backup.sql

Run one of the following commands depending on your operating system:

Mac/Linux:
```bash
docker-compose exec -T db psql -U postgres -d ai_use_cases -p 5433 < backup.sql
```

Windows:
```bash
type backup.sql | docker-compose exec -T db psql -U postgres -d ai_use_cases -p 5433
```

### 4. Sync Elasticsearch with Initial Data
```bash
docker-compose exec backend python3 sync_elasticsearch.py
```

## Troubleshooting

### Check container logs with:

```bash
docker-compose logs -f <service_name>
```

### Verify running services with:

```bash
docker-compose ps
```

## Learn More
[Docker Compose Documentation](https://docs.docker.com/compose/?spm=a2ty_o01.29997173.0.0.1ba1c921fPwE1A)

[Docker Best Practices](https://docs.docker.com/build/building/best-practices/)

