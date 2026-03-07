# E-Commerce Backend

A production-ready **FastAPI backend** built with **PostgreSQL**, **Alembic migrations**, **Redis**, and **Docker**.  
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
git clone https://github.com/VinayParmar555/E-commerce.git
cd E-commerce
```

### 2. Create environment variables
```bash
DATABASE_URL="postgresql://postgres:yourpassword@postgres:5432/yourdbname"
DATABASE_NAME=yourdbname
DATABASE_USER=postgres
DATABASE_PWD=yourpassword

JWT_SECRET_KEY=your_jwt_secret_key
JWT_REFRESH_SECRET_KEY=your_jwt_refresh_secret_key
JWT_EMAIL_SECRET_KEY=your_jwt_email_secret_key

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
EMAIL_TOKEN_EXPIRE_MINUTES=60

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
RAZORPAY_WEBHOOK_SECRET=your_razorpay_webhook_secret

SENDGRID_API_KEY=SG.your_sendgrid_api_key
FROM_EMAIL=your_email@example.com

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
The application is deployed on Render directly from github repository.
- Source: GitHub repository  
- Build & Deploy: Managed by Render  
- Auto-deploy enabled on every push to `main` branch 

```bash
https://e-commerce-ytgi.onrender.com/docs
```









