# E-Commerce Backend

[![CI/CD](https://github.com/VinayParmar555/E-commerce/actions/workflows/test.yml/badge.svg)](https://github.com/VinayParmar555/E-commerce/actions)
[![codecov](https://codecov.io/gh/VinayParmar555/E-commerce/badge.svg)](https://codecov.io/gh/VinayParmar555/E-commerce)

A production-ready **FastAPI backend** built with **PostgreSQL**, **Alembic migrations**, **Redis**, and **Docker**.  
The application is fully containerized and deployed on **Render**.

---

## Features

- **JWT Authentication** — Access tokens + refresh token rotation with secure httponly cookies
- **Email Verification** — Background email verification via SendGrid
- **Role-Based Access Control** — Centralized `get_current_user` dependency for admin-only routes
- **Product Management** — Full CRUD with category support, bulk import, pagination & filtering
- **Shopping Cart** — Add, view, update, and remove cart items with stock validation
- **Order & Checkout** — Cart-to-order flow with address validation and atomic stock deduction
- **Payment Integration** — Razorpay (live) + mock gateway for testing; webhook with HMAC verification
- **Shipping Management** — Address CRUD and order shipping status tracking
- **Redis Caching** — Product listing cache with msgpack serialization and TTL-based invalidation
- **Rate Limiting** — Redis-backed rate limiter with IP and user-level strategies
- **Input Validation** — Pydantic schemas with field-level constraints (min/max length, value ranges)
- **Refresh Token Cleanup** — Automatic cleanup of expired/revoked tokens on app startup
- **Database Migrations** — 13 Alembic migration versions with full schema history
- **Docker & CI/CD** — Multi-service Docker Compose, GitHub Actions pipeline, Codecov integration

---

## API Endpoints

### Authentication (`/account`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/account/register` | Register a new user |
| POST | `/account/login` | Login and receive tokens |
| POST | `/account/refresh` | Refresh access token |
| POST | `/account/verify-request` | Send email verification link |
| GET | `/account/verify` | Verify email with token |

### User Profile (`/profile`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profile/me` | Get current user profile |
| PUT | `/profile/change-password` | Change password |
| POST | `/profile/forgot-password` | Request password reset |
| POST | `/profile/set-password` | Set new password with reset token |
| POST | `/profile/make-admin` | Promote user to admin (admin only) |
| POST | `/profile/logout` | Logout and revoke refresh token |
| DELETE | `/profile/delete` | Delete account |

### Products (`/products`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products/all` | List all products (cached) |
| GET | `/products/search/{id}` | Search product by ID |
| POST | `/products/add_product` | Add product (admin only) |
| PUT | `/products/update/{id}` | Update product (admin only) |
| DELETE | `/products/delete/{id}` | Delete product (admin only) |
| POST | `/products/bulk_products` | Bulk add products (admin only) |
| GET | `/products/pagination` | Paginated product list |
| GET | `/products/filter` | Filter by category, name, price range |

### Categories (`/Categories`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/Categories/add` | Add category (admin only) |
| GET | `/Categories/all` | List all categories |
| PUT | `/Categories/update` | Update category (admin only) |
| DELETE | `/Categories/delete/{id}` | Delete category (admin only) |

### Cart (`/Cart`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/Cart/add_cart` | Add item to cart |
| GET | `/Cart/see_cart` | View cart contents |
| DELETE | `/Cart/delete_cart/{cart_id}` | Remove item from cart |

### Orders (`/order`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/order/checkout` | Checkout and place order |
| GET | `/order/fetch_placed_order` | Get all placed orders |
| GET | `/order/single_placed_order/{id}` | Get single order details |
| PATCH | `/order/cancel/{order_id}` | Cancel an order |
| GET | `/order/shipping_status/{order_id}` | Get shipping status |
| PATCH | `/order/update_shipping_status/{id}` | Update shipping status (admin only) |

### Shipping Addresses (`/shipping_addresses`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shipping_addresses/add` | Add shipping address |
| GET | `/shipping_addresses/fetch` | Get all addresses |
| GET | `/shipping_addresses/fetch_byid/{id}` | Get address by ID |
| PUT | `/shipping_addresses/update/{id}` | Update address |
| DELETE | `/shipping_addresses/delete/{id}` | Delete address |

### Payments (`/payment`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payment/razorpay/webhook` | Razorpay webhook handler |
| PATCH | `/payment/status/{order_id}` | Check payment status |
| PATCH | `/payment/status/all` | Check all payment statuses |

---

## Tech Stack

- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Migrations:** Alembic (13 versions)
- **Cache:** Redis with msgpack serialization
- **Auth:** JWT (access + refresh tokens) + bcrypt
- **Payments:** Razorpay + Mock gateway
- **Email:** SendGrid
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions → Codecov → Render

---

## Getting Started

You can run this project in two ways:

1. **Local Development (Docker)**
2. **Production (Deployed on Render)**

---

## Local Development (Docker)

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
Create a `.env` file in the project root:
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
docker compose up --build --no-cache
```
This will start your:
- FastAPI application
- PostgreSQL database
- Redis cache

### 4. Run the Application (Swagger API Docs)
```
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
- Build & Deploy: Managed by Render using Dockerfile  
- Auto-deploy enabled on every push to `main` branch 

```bash
https://e-commerce-ytgi.onrender.com/docs
```









