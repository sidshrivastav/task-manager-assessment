
# 📝 Task Manager API

A Django REST Framework (DRF) based task manager that supports background processing using Celery and Redis.

---

## 🚀 Features

- REST APIs for task CRUD
- Asynchronous task processing with Celery
- MySQL for persistent storage
- Redis as Celery broker
- Dockerized setup

---

## 🧱 Project Structure

```
.
├── app/                   # Main Django project
├── task/                  # App containing task logic
├── Dockerfile
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── docker-compose.yml
├── requirements.txt
├── .env
├── manage.py
└── README.md
```

---

## 🔧 Requirements

- Docker + Docker Compose
- Python 3.13 (for local development without Docker)

---

## ⚙️ Environment Setup

Create a `.env` file in the root directory:

```env
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=True
MYSQL_DATABASE=mydb
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_HOST=db
MYSQL_PORT=3306
```

---

## 🐳 Docker Setup

### ✅ Build and run all services

```bash
docker-compose up --build -d
```

- Django will run on: `http://localhost:8000`
- Swagger will run on: `http://localhost:8000/swagger`
- MySQL will be available on: `localhost:3306`
- Redis will run on: `localhost:6379`

---

## 🛠️ Apply Migrations

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

---

## 📮 API Endpoints

| Method | Endpoint           | Description                     |
|--------|--------------------|---------------------------------|
| POST   | `/api/tasks/`      | Create a new task               |
| GET    | `/api/tasks/`      | List all tasks                  |
| GET    | `/api/tasks/<id>/` | Retrieve a task by ID           |
| PATCH  | `/api/tasks/<id>/` | Partial Update a task completely|
| DELETE | `/api/tasks/<id>/` | Delete a task                   |

When a task is created, a background Celery job will:
- Mark it as `in_progress`
- Wait 5 seconds
- Then mark it as `completed`

---

## ⚙️ Run Celery Worker

In a separate terminal:

```bash
docker-compose exec web celery -A task_manager worker --loglevel=info
```

Or ensure the celery service is enabled in `docker-compose.yml`:

```yaml
celery:
  build: .
  command: celery -A task_manager worker --loglevel=info
  volumes:
    - .:/app
  depends_on:
    - redis
    - db
  env_file:
    - .env
```

---

## 🧪 Running Tests

### 🔹 Run tests using SQLite in-memory DB

Edit `settings.py`:

```python
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
```

Then run:

```bash
docker-compose exec web python manage.py test
```

---

## 📊 Run Test Coverage

```bash
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

(Optional) generate HTML report:

```bash
docker-compose exec web coverage html
```

Open `htmlcov/index.html` in your browser.

---

## ✨ Tips

- To access MySQL inside the container:

```bash
docker-compose exec db mysql -u root -p
```

---

## 🧹 Cleanup

To remove containers, networks, and volumes:

```bash
docker-compose down -v
```
