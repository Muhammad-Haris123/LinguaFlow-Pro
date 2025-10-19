# Deployment Guide

This guide covers different deployment options for the Multilingual Translation Service.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Node.js 16+ (for frontend development)
- CUDA-compatible GPU (recommended for training)

## Local Development

### 1. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start the frontend
npm start
```

### 3. Training a Model

```bash
# Train with default configuration
python training/train.py

# Train with custom configuration
python training/train.py --config configs/custom_config.yaml

# Resume from checkpoint
python training/train.py --resume checkpoints/checkpoint_epoch_5.pt
```

## Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f translator

# Stop services
docker-compose down
```

### 2. Manual Docker Build

```bash
# Build the image
docker build -t multilingual-translator .

# Run the container
docker run -p 8000:8000 multilingual-translator

# Run with GPU support
docker run --gpus all -p 8000:8000 multilingual-translator
```

## Cloud Deployment

### AWS Deployment

#### Option 1: EC2 Instance

1. **Launch EC2 Instance**
   - Choose GPU-enabled instance (e.g., p3.2xlarge)
   - Install Docker and Docker Compose
   - Configure security groups (ports 80, 443, 8000)

2. **Deploy Application**
   ```bash
   git clone <repository-url>
   cd Translator
   docker-compose up -d
   ```

3. **Configure Load Balancer**
   - Use Application Load Balancer
   - Set up SSL certificate
   - Configure health checks

#### Option 2: ECS with Fargate

1. **Create ECS Cluster**
   ```bash
   aws ecs create-cluster --cluster-name translator-cluster
   ```

2. **Build and Push Image**
   ```bash
   aws ecr create-repository --repository-name multilingual-translator
   docker build -t multilingual-translator .
   docker tag multilingual-translator:latest <account>.dkr.ecr.<region>.amazonaws.com/multilingual-translator:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/multilingual-translator:latest
   ```

3. **Create Task Definition**
   - Define container specifications
   - Set up environment variables
   - Configure logging

4. **Create Service**
   - Configure auto-scaling
   - Set up load balancer
   - Configure health checks

### Google Cloud Platform

#### Option 1: Compute Engine

1. **Create VM Instance**
   ```bash
   gcloud compute instances create translator-vm \
     --image-family=cos-stable \
     --image-project=cos-cloud \
     --machine-type=n1-standard-4 \
     --accelerator=type=nvidia-tesla-t4,count=1 \
     --boot-disk-size=50GB
   ```

2. **Install Docker and Deploy**
   ```bash
   # Install Docker
   curl -fsSL https://get.docker.com | sh
   
   # Deploy application
   git clone <repository-url>
   cd Translator
   docker-compose up -d
   ```

#### Option 2: Cloud Run

1. **Build and Push Image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/multilingual-translator
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy multilingual-translator \
     --image gcr.io/PROJECT_ID/multilingual-translator \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Azure Deployment

#### Option 1: Container Instances

1. **Create Resource Group**
   ```bash
   az group create --name translator-rg --location eastus
   ```

2. **Deploy Container**
   ```bash
   az container create \
     --resource-group translator-rg \
     --name translator-app \
     --image multilingual-translator:latest \
     --ports 8000 \
     --cpu 2 \
     --memory 4
   ```

#### Option 2: Azure Kubernetes Service

1. **Create AKS Cluster**
   ```bash
   az aks create \
     --resource-group translator-rg \
     --name translator-aks \
     --node-count 2 \
     --enable-addons monitoring
   ```

2. **Deploy Application**
   ```bash
   kubectl apply -f k8s/
   ```

## Production Considerations

### 1. Security

- Use HTTPS with SSL certificates
- Implement authentication and authorization
- Set up rate limiting
- Use secrets management for API keys
- Regular security updates

### 2. Monitoring

- Set up application monitoring (e.g., Prometheus, Grafana)
- Configure log aggregation (e.g., ELK stack)
- Set up alerting for critical issues
- Monitor resource usage and performance

### 3. Scaling

- Implement horizontal pod autoscaling
- Use load balancers for traffic distribution
- Consider using CDN for static assets
- Implement caching strategies

### 4. Backup and Recovery

- Regular database backups
- Model checkpoint backups
- Disaster recovery procedures
- Data retention policies

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `MODEL_PATH` | Path to trained model | `./checkpoints/best_model.pt` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAX_WORKERS` | Maximum worker processes | `4` |
| `CACHE_TTL` | Cache time-to-live (seconds) | `3600` |

## Health Checks

The application provides several health check endpoints:

- `GET /health` - Overall application health
- `GET /languages` - Available languages
- `GET /model/info` - Model information

## Troubleshooting

### Common Issues

1. **GPU Not Available**
   - Ensure CUDA is properly installed
   - Check GPU memory availability
   - Verify PyTorch CUDA installation

2. **Memory Issues**
   - Reduce batch size
   - Use gradient accumulation
   - Enable mixed precision training

3. **Slow Performance**
   - Check Redis connectivity
   - Optimize model inference
   - Use model quantization

### Logs

- Application logs: `./logs/`
- Docker logs: `docker-compose logs`
- System logs: Check system journal

## Support

For deployment issues:
1. Check the logs
2. Verify configuration
3. Test individual components
4. Consult the troubleshooting guide
5. Open an issue on GitHub



