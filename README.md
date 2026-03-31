# 🏥 Medical Records API

A **production-ready REST API** built with FastAPI and PostgreSQL — created as a **free alternative practice API** for developers who want to learn REST API consumption, authentication flows, and CRUD operations without paying for third-party services.

> **Note:** This is a **practice/learning API**. It is intentionally open for developers to use as a sandbox for testing API consumption, JWT authentication, and CRUD operations. Most practice APIs online require paid subscriptions — this one is free.

---

## 🌐 Live API

```
Base URL:  https://medical-records-api.onrender.com
Docs:      https://medical-records-api.onrender.com/docs
ReDoc:     https://medical-records-api.onrender.com/redoc
```

> ⚠️ Hosted on Render's free tier — first request may take ~30 seconds to wake up.

---

## ✨ Features

- 🔐 **JWT Authentication** — OAuth2 password flow with Bearer tokens
- 👨‍⚕️ **Doctors** — Full CRUD with one-to-many relationship to records
- 📋 **Medical Records** — Full CRUD with filtering, pagination, and validation
- ✅ **Data Validation** — Pydantic models with strict field validation
- 🗄️ **PostgreSQL** — Production database with SQLAlchemy ORM
- 🐳 **Docker** — Fully containerized with docker-compose
- 🧪 **Testing** — 90%+ test coverage with pytest
- 📖 **Auto Docs** — Swagger UI and ReDoc out of the box

---

## 🚀 Quick Start — Using the API

### Step 1 — Login and get a token

```bash
curl -X POST https://medical-records-api.onrender.com/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secret123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Step 2 — Use the token in requests

```bash
curl https://medical-records-api.onrender.com/records/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..."
```

---

## 👤 Test Credentials

Use these pre-created accounts to explore the API:

| Username | Password   |
|----------|------------|
| john     | secret123  |
| jane     | password456 |

---

## 📌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/token` | Login — returns JWT token |
| `GET`  | `/me`    | Get current logged in user |

### Doctors
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST`   | `/doctors/`         | Create a doctor |
| `GET`    | `/doctors/`         | List all doctors |
| `GET`    | `/doctors/{id}`     | Get doctor + their records |
| `DELETE` | `/doctors/{id}`     | Delete a doctor |

### Medical Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST`   | `/records/`         | Create a record |
| `GET`    | `/records/`         | List all records (filterable) |
| `GET`    | `/records/{id}`     | Get a single record |
| `PUT`    | `/records/{id}`     | Full update |
| `DELETE` | `/records/{id}`     | Delete a record |

---

## 🔍 Filtering & Pagination

```bash
# Filter by doctor name
GET /records/?doctor=Dr.+Smith

# Filter by blood type
GET /records/?blood_type=A%2B

# Pagination
GET /records/?limit=5&offset=10

# Combine filters
GET /records/?blood_type=O%2B&limit=10&offset=0
```

---

## 📝 Example — Create a Doctor

```bash
curl -X POST https://medical-records-api.onrender.com/doctors/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Sarah Johnson",
    "email": "sarah.johnson@hospital.com",
    "specialization": "Cardiology",
    "phone": "+14155552671"
  }'
```

## 📝 Example — Create a Medical Record

```bash
curl -X POST https://medical-records-api.onrender.com/records/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "John Doe",
    "age": 30,
    "blood_type": "A+",
    "diagnosis": "Hypertension",
    "doctor_id": 1,
    "email": "john.doe@example.com",
    "phone": "+14155552671",
    "admitted_at": "2024-01-15T09:00:00",
    "is_admitted": true,
    "notes": "Patient responding well to treatment",
    "weight": 75.5,
    "height": 175.0
  }'
```

---

## 🩸 Valid Blood Types

```
A+  A-  B+  B-  AB+  AB-  O+  O-
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **PostgreSQL** | Database |
| **SQLAlchemy** | ORM |
| **Alembic** | Database migrations |
| **Pydantic** | Data validation |
| **JWT / OAuth2** | Authentication |
| **bcrypt** | Password hashing |
| **pytest** | Testing (90%+ coverage) |
| **Docker** | Containerization |
| **Render** | Cloud deployment |

---

## 🏃 Run Locally

### With Docker (recommended):

```bash
# Clone the repo
git clone https://github.com/ganesh040/MedicalrecordsAPI
cd MedicalrecordsAPI

# Start everything
docker compose up --build

# API available at:
http://localhost:8000/docs
```

### Without Docker:

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/medical_records

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

---

## 🧪 Running Tests

```bash
pytest test_records.py -v --cov=. --cov-report=term-missing
```

---

## 📁 Project Structure

```
MedicalrecordsAPI/
├── main.py              # FastAPI app, middleware, routers
├── database.py          # SQLAlchemy engine, session, Base
├── models.py            # SQLAlchemy DB models (tables)
├── security.py          # JWT, password hashing
├── test_records.py      # pytest test suite
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image instructions
├── docker-compose.yml   # Multi-container setup
├── .dockerignore        # Docker ignore rules
├── alembic/             # Database migrations
├── routers/
│   ├── applications.py  # Medical records endpoints
│   ├── auth.py          # Login, JWT endpoints
│   └── doctors.py       # Doctors endpoints
└── schemas/
    └── records.py       # Pydantic validation models
```

---

## 🎯 Why This API Exists

Most REST API practice platforms (like ReqRes, JSONPlaceholder) are either:
- Too simple (no auth, no real CRUD)
- Paywalled for advanced features
- Read-only

This API was built to give developers a **free, realistic sandbox** with:
- ✅ Real JWT authentication flow
- ✅ Full CRUD operations
- ✅ Data validation and error handling
- ✅ Relational data (doctors → records)
- ✅ Filtering and pagination
- ✅ Proper HTTP status codes
- ✅ OpenAPI/Swagger documentation

---

## ⚠️ Disclaimer

This is a **practice API** with fake medical data. Do not use it to store real patient information. Data may be reset periodically.

---

## 👨‍💻 Author

**Ganesh Reddy Gudibandi**
- GitHub: [@ganesh040](https://github.com/ganesh040)
- Portfolio: [ganeshreddygudibandi.com](https://ganeshreddygudibandi.com)
- LinkedIn: [Connect with me](https://linkedin.com/in/ganeshreddygudibandi)

---

## 📄 License

MIT License — free to use for learning and practice.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if any)
5. Submit a pull request

## License

This project is licensed under the MIT License.
