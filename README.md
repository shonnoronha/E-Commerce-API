# E-Commerce API

### A Simple Market-Place like API implemented using FastAPI

## To Run this Project Locally

### Config Ecommerce project

#### Create .env file at the root of project and set following options

#### You can create a secrey key by executing `openssl rand -hex 32`

```sh
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_USERNAME=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
ADMIN_EMAIL=
```

### 1.Clone This Repository

```sh
git clone https://github.com/shonnoronha/ecommerce-backend.git
cd ecommerce-backend
```

### 2. Docker (Recommended)

```sh
docker-compose up -d
docker exec ecommerce alembic upgrade head
```

### OR

### 2. Install manually

#### you will need a postgres database (check config below) and python 3.9+

```sh
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app
```

### 3. Open Docs

### Visit [localhost:8000/docs](http://localhost:8000/docs)

### Create a Customer with Admin Email

### Login using Admin Email

## Database Design

![database-schema](./assets/db_schema.png)
