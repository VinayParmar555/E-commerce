# E-Commerce Backend

A production-ready **FastAPI backend** built with **PostgreSQL**, **Redis**, and **Docker**.  
The application is fully containerized and deployed on **Render**.

---

## Here we go

You can run this project in two ways:

1. **Local Development (Docker)**
2. **Production (Deployed on Render)**

---

##  Local Development (Docker)

### Prerequisites
- Docker
- Docker Compose

---

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd E-commerce_backup
```

### 2. Create environment variables
```bash
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/your_db_name

POSTGRES_DB=your_db_name
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

JWT_SECRET_KEY=your_secret
JWT_REFRESH_SECRET_KEY=your_refresh_secret
JWT_EMAIL_SECRET_KEY=your_email_secret
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
EMAIL_TOKEN_EXPIRE_MINUTES=10
```
### 3. Start the development server
```bash
docker compose up -d
```
This will start your:
- FastAPI application
- PostgreSQL database
- Redis cache
### 4. Run the Application (Swagger API Docs)
```bash
http://localhost:8000/docs
```
### 5. View logs
```bash
docker logs -f e-commerce_app
```
### 6. Stop the application
```bash
docker compose stop
```
This stops containers but keeps database data intact.

### 7. Production Deployment (Render)
The application is deployed on Render using a Docker image pushed to Docker Hub.
```bash
https://e-commerce-ytgi.onrender.com/docs
```









