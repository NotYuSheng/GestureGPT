# GestureGPT Deployment Guide

This guide covers deploying GestureGPT using Docker and GitHub Container Registry (GHCR).

## Quick Start with Docker Compose

### 1. Using Pre-built Image from GHCR

```bash
# Pull and run the backend only
docker-compose up -d

# Or run with the Streamlit demo
docker-compose --profile demo up -d
```

The backend API will be available at `http://localhost:8000`
The demo (if enabled) will be at `http://localhost:8501`

### 2. Building Locally

If you want to build the image yourself:

```bash
# Build the backend image
docker build -t gesturegpt:local .

# Update docker-compose.yml to use local image
# Change: image: ghcr.io/notyusheng/gesturegpt:latest
# To: image: gesturegpt:local

# Run with docker-compose
docker-compose up -d
```

## Manual Docker Commands

### Backend API

```bash
# Pull from GHCR
docker pull ghcr.io/notyusheng/gesturegpt:latest

# Run the container
docker run -d \
  --name gesturegpt-backend \
  -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/static:/app/static \
  -e API_TITLE="GestureGPT" \
  ghcr.io/notyusheng/gesturegpt:latest

# Check logs
docker logs -f gesturegpt-backend

# Stop and remove
docker stop gesturegpt-backend
docker rm gesturegpt-backend
```

### Streamlit Demo

```bash
# Build the demo image
docker build -f Dockerfile.demo -t gesturegpt-demo .

# Run the demo
docker run -d \
  --name gesturegpt-demo \
  -p 8501:8501 \
  -e SIGNALAPI_URL=http://backend:8000 \
  --network gesturegpt-network \
  gesturegpt-demo

# Check logs
docker logs -f gesturegpt-demo
```

## GitHub Container Registry (GHCR)

### Automatic Build with GitHub Actions

The project includes a GitHub Actions workflow that automatically builds and pushes to GHCR on:
- Push to `main` branch
- New tags (e.g., `v1.0.0`)
- Manual workflow dispatch

The workflow is defined in [.github/workflows/docker-publish.yml](.github/workflows/docker-publish.yml)

### Image Versioning

Images are tagged with:
- `latest` - Latest commit to main branch
- `main` - Latest commit to main branch
- `v1.0.0` - Semantic version tags
- `sha-<commit>` - Specific commit SHA

### Pulling Different Versions

```bash
# Latest version
docker pull ghcr.io/notyusheng/gesturegpt:latest

# Specific version
docker pull ghcr.io/notyusheng/gesturegpt:v1.0.0

# Specific commit
docker pull ghcr.io/notyusheng/gesturegpt:main-abc1234
```

## Environment Variables

Configure the application using environment variables:

```bash
# Server
HOST=0.0.0.0
PORT=8000

# API
API_TITLE=GestureGPT
API_VERSION=1.0.0
API_DESCRIPTION=Sign Language LLM-style API

# Sign Language
MAX_TEXT_LENGTH=500
DEFAULT_VIDEO_FORMAT=mp4
ENABLE_GIF_CONVERSION=true

# Storage
VIDEO_OUTPUT_DIR=./output/videos
STATIC_FILES_DIR=./static
```

## Volume Mounts

The following volumes should be mounted for persistent storage:

- `./output:/app/output` - Generated videos
- `./static:/app/static` - Static files

## Health Checks

The container includes health checks:

```bash
# Check container health
docker ps

# Manual health check
curl http://localhost:8000/health
```

## Production Deployment

### Docker Compose Production

```yaml
version: '3.8'

services:
  backend:
    image: ghcr.io/notyusheng/gesturegpt:latest
    container_name: gesturegpt-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - API_TITLE=GestureGPT
    volumes:
      - gesturegpt-output:/app/output
      - gesturegpt-static:/app/static
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

volumes:
  gesturegpt-output:
  gesturegpt-static:

networks:
  default:
    name: gesturegpt-network
```

### Behind Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # For video files
    location /videos/ {
        proxy_pass http://localhost:8000/videos/;
        proxy_buffering off;
    }

    # For Streamlit demo
    location /demo/ {
        proxy_pass http://localhost:8501/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gesturegpt-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gesturegpt
  template:
    metadata:
      labels:
        app: gesturegpt
    spec:
      containers:
      - name: backend
        image: ghcr.io/notyusheng/gesturegpt:latest
        ports:
        - containerPort: 8000
        env:
        - name: HOST
          value: "0.0.0.0"
        - name: PORT
          value: "8000"
        volumeMounts:
        - name: output
          mountPath: /app/output
        - name: static
          mountPath: /app/static
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
      volumes:
      - name: output
        persistentVolumeClaim:
          claimName: gesturegpt-output
      - name: static
        persistentVolumeClaim:
          claimName: gesturegpt-static
---
apiVersion: v1
kind: Service
metadata:
  name: gesturegpt-service
spec:
  selector:
    app: gesturegpt
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Monitoring and Logs

### View Logs

```bash
# Docker Compose
docker-compose logs -f backend

# Docker
docker logs -f gesturegpt-backend

# Last 100 lines
docker logs --tail 100 gesturegpt-backend
```

### Resource Monitoring

```bash
# Container stats
docker stats gesturegpt-backend

# Detailed inspection
docker inspect gesturegpt-backend
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs gesturegpt-backend

# Check if port is already in use
lsof -i :8000

# Restart container
docker restart gesturegpt-backend
```

### API Not Responding

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check if container is running
docker ps | grep gesturegpt

# Enter container for debugging
docker exec -it gesturegpt-backend /bin/bash
```

### Video Generation Issues

```bash
# Check volume mounts
docker inspect gesturegpt-backend | grep Mounts -A 10

# Check disk space
df -h

# Check permissions
ls -la output/ static/
```

## Updating

### Update to Latest Version

```bash
# Pull latest image
docker pull ghcr.io/notyusheng/gesturegpt:latest

# Restart with docker-compose
docker-compose down
docker-compose up -d

# Or with docker
docker stop gesturegpt-backend
docker rm gesturegpt-backend
docker run -d \
  --name gesturegpt-backend \
  -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  ghcr.io/notyusheng/gesturegpt:latest
```

## Development

### Building and Testing Locally

```bash
# Build the image
docker build -t gesturegpt:dev .

# Run tests (if you add them)
docker run --rm gesturegpt:dev pytest

# Run with development settings
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  -e DEBUG=true \
  gesturegpt:dev
```

## Security

### Best Practices

1. **Use specific image tags** instead of `latest` in production
2. **Scan images** for vulnerabilities: `docker scan ghcr.io/notyusheng/gesturegpt:latest`
3. **Limit container resources**: Add `--memory` and `--cpus` flags
4. **Use read-only filesystem** where possible: `--read-only`
5. **Run as non-root** (already configured in Dockerfile)
6. **Enable TLS** when deploying publicly

### Example with Resource Limits

```bash
docker run -d \
  --name gesturegpt-backend \
  -p 8000:8000 \
  --memory="512m" \
  --cpus="1.0" \
  --restart=unless-stopped \
  ghcr.io/notyusheng/gesturegpt:latest
```
