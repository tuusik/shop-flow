# ShopFlow Roadmap

## Project Goal

Build a production-style backend application while learning:

* SQLAlchemy 2.0
* PostgreSQL
* FastAPI
* ORM relationships
* Database design
* Backend architecture
* Authentication
* Async programming

The primary goal is not to build a perfect online store.

The primary goal is to understand how modern backend applications are built.

---

# Milestone 0 — Project Setup

## Goal

Launch a working FastAPI application.

## Tasks

* Create repository
* Create virtual environment
* Install dependencies
* Create FastAPI application
* Run server locally

## Definition of Done

Endpoint works:

```http
GET /
```

returns:

```json
{
  "status": "ok"
}
```

---

# Milestone 1 — Database Basics

## Goal

Learn SQLAlchemy fundamentals.

## Tasks

Create:

* PostgreSQL container
* database connection
* Base class
* Session factory

Create first model:

### User

Fields:

* id
* email
* created_at

## Definition of Done

User table exists in database.

---

# Milestone 2 — User CRUD

## Goal

Learn ORM operations.

## Tasks

Implement:

### Create User

```http
POST /users
```

### Get Users

```http
GET /users
```

### Get User By Id

```http
GET /users/{id}
```

### Delete User

```http
DELETE /users/{id}
```

## SQLAlchemy Concepts

* Session
* add
* commit
* refresh
* select
* where

---

# Milestone 3 — Product CRUD

## Goal

Work with multiple models.

## Tasks

Create Product model.

Fields:

* id
* title
* description
* price
* stock
* created_at

Implement CRUD endpoints.

## Definition of Done

Products can be created, updated, listed and deleted.

---

# Milestone 4 — Relationships

## Goal

Learn ORM relationships.

## Tasks

Create:

### Order

Fields:

* id
* user_id
* created_at

### OrderItem

Fields:

* id
* order_id
* product_id
* quantity

Implement relationships:

* User -> Orders
* Order -> User
* Order -> Items
* Product -> OrderItems

## Definition of Done

Orders can contain multiple products.

---

# Milestone 5 — Queries

## Goal

Learn how to use SQLAlchemy efficiently.

## Tasks

Implement:

### Get user orders

### Get products in order

### Get all orders with user data

### Get popular products

## Concepts

* joins
* eager loading
* selectinload
* joinedload

---

# Milestone 6 — Project Structure

## Goal

Separate responsibilities.

## Tasks

Create folders:

```text
app/
├── api/
├── db/
├── models/
├── schemas/
├── repositories/
├── services/
└── core/
```

Move business logic from endpoints into services.

Move database access into repositories.

---

# Milestone 7 — Alembic

## Goal

Manage schema changes correctly.

## Tasks

* Initialize Alembic
* Configure migrations
* Generate first migration
* Apply migrations

## Definition of Done

Database schema is created only through migrations.

---

# Milestone 8 — Authentication

## Goal

Protect API.

## Tasks

Implement:

* registration
* login
* JWT tokens
* current user endpoint

Add:

* password hashing
* protected routes

---

# Milestone 9 — Async SQLAlchemy

## Goal

Use modern async backend stack.

## Tasks

Replace sync implementation with:

* AsyncEngine
* AsyncSession
* asyncpg

## Definition of Done

All database operations are asynchronous.

---

# Milestone 10 — Production Features

## Tasks

Add:

* pagination
* filtering
* sorting
* category support
* many-to-many relationships

Optional:

* Redis
* Celery
* Dockerfile
* CI/CD

---

# Final Project Requirements

The project should demonstrate:

* SQLAlchemy 2.0
* ORM relationships
* Repository pattern
* Service layer
* PostgreSQL
* Alembic
* Authentication
* Async programming
* Clean architecture

The goal is to create a portfolio-quality backend project rather than a simple CRUD tutorial.
