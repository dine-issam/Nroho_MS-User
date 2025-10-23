# Microservices Architecture with Spring Cloud & Django

A microservices-based application featuring Spring Cloud Gateway, Eureka Service Discovery, Firebase Authentication, and a Django user management service.

## Architecture Overview

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   API Gateway (Spring Cloud)    │
│   Port: 7777                    │
│   - JWT Authentication          │
│   - Route Management            │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Eureka Server                 │
│   Port: 8888                    │
│   - Service Discovery           │
└─────────────────────────────────┘
         │
         ├──────────────┐
         ▼              ▼
┌──────────────┐  ┌──────────────┐
│  ms-user     │  │  PostgreSQL  │
│  (Django)    │──│  Database    │
│  Port: 8000  │  │  Port: 5432  │
└──────────────┘  └──────────────┘
```

## Services

### 1. Eureka Server
- **Port**: 8888
- **Purpose**: Service discovery and registration
- **Technology**: Spring Cloud Netflix Eureka

### 2. API Gateway
- **Port**: 7777
- **Purpose**: Single entry point, routing, and authentication
- **Technology**: Spring Cloud Gateway
- **Features**:
  - Firebase JWT authentication
  - Request routing to microservices
  - Security configuration

### 3. User Microservice (ms-user)
- **Port**: 8000
- **Purpose**: User management and authentication
- **Technology**: Django REST Framework
- **Features**:
  - User CRUD operations
  - Chat and message management
  - Firebase authentication integration
  - PostgreSQL database

## Tech Stack

- **Java**: 21
- **Spring Boot**: 3.5.6
- **Spring Cloud**: 2025.0.0
- **Python**: 3.10
- **Django**: 5.2.6
- **PostgreSQL**: 14.18
- **Firebase Admin SDK**: For authentication
- **Docker & Docker Compose**: For containerization

## Prerequisites

- Java 21+
- Python 3.10+
- Docker & Docker Compose
- Maven 3.9+
- Firebase project with service account key

## Setup Instructions

### 1. Firebase Configuration

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Generate a service account key:
   - Go to Project Settings → Service Accounts
   - Click "Generate New Private Key"
3. Place the key files:
   - `gateway-api/src/main/resources/serviceAccountKey.json`
   - `ms_user/ms_user/serviceAccountKey.json`

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Firebase
FIREBASE_API_KEY=your_firebase_api_key

# Django
SECRET_KEY=your_django_secret_key

# PostgreSQL
PG_USER=postgres
PG_PASSWORD=yourpassword
PG_DB=mydb
PG_PORT=5432
PG_HOST=my-postgres
```

### 3. Build Services

#### Build Eureka Server
```bash
cd eureka
./mvnw clean package
cd ..
```

#### Build API Gateway
```bash
cd gateway-api
./mvnw clean package
cd ..
```

#### Build Django Service
```bash
cd ms_user
pip install -r requirements.txt
python manage.py migrate
cd ..
```

### 4. Run with Docker Compose

```bash
docker-compose up --build
```

This will start:
- Eureka Server on port 8888
- API Gateway on port 7777
- ms-user service on port 8000
- PostgreSQL on port 5432

### 5. Run Locally (Development)

#### Start Eureka Server
```bash
cd eureka
./mvnw spring-boot:run
```

#### Start API Gateway
```bash
cd gateway-api
./mvnw spring-boot:run
```

#### Start Django Service
```bash
cd ms_user
python manage.py runserver 8000
```

#### Start PostgreSQL
```bash
docker run -d \
  --name my-postgres \
  -e POSTGRES_DB=mydb \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -p 5432:5432 \
  postgres:14.18-bookworm
```

## API Endpoints

All requests go through the API Gateway at `http://localhost:7777`

### Authentication (No JWT Required)

#### Sign Up
```http
POST /ms-user/auth/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "plan": "FREE"
}
```

#### Sign In
```http
POST /ms-user/auth/signin/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response includes**:
- `idToken`: JWT token for authentication
- `refreshToken`: Token for refreshing expired JWT
- `user`: User object with details

### Authenticated Endpoints (Requires JWT)

Add the JWT token to all subsequent requests:
```http
Authorization: Bearer <idToken>
```

#### Users
- `GET /ms-user/users/` - List all users
- `GET /ms-user/users/{id}/` - Get user by ID
- `POST /ms-user/users/create/` - Create user
- `PUT /ms-user/users/update/{id}/` - Update user
- `DELETE /ms-user/users/delete/{id}/` - Delete user

#### Chats
- `GET /ms-user/chats/` - List all chats
- `GET /ms-user/chats/{id}/` - Get chat by ID
- `POST /ms-user/chats/create/` - Create chat
- `PUT /ms-user/chats/update/{id}/` - Update chat
- `DELETE /ms-user/chats/delete/{id}/` - Delete chat

#### Messages
- `GET /ms-user/messages/` - List all messages
- `GET /ms-user/messages/chat/{chat_id}/` - Get messages by chat
- `GET /ms-user/messages/{id}/` - Get message by ID
- `POST /ms-user/messages/create/` - Create message
- `PUT /ms-user/messages/update/{id}/` - Update message
- `DELETE /ms-user/messages/delete/{id}/` - Delete message

## Project Structure

```
.
├── eureka/                      # Eureka service discovery
│   ├── src/
│   ├── pom.xml
│   └── dockerfile
├── gateway-api/                 # API Gateway
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/example/gateway_api/
│   │       │       ├── auth/
│   │       │       │   ├── config/
│   │       │       │   └── filter/
│   │       │       └── GatewayApiApplication.java
│   │       └── resources/
│   │           ├── application.yml
│   │           └── serviceAccountKey.json
│   ├── pom.xml
│   └── dockerfile
├── ms_user/                     # Django user service
│   ├── ms_user/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── middlewares.py
│   │   └── serviceAccountKey.json
│   ├── userapp/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── eureka_client.py
│   ├── requirements.txt
│   ├── manage.py
│   └── dockerfile
├── docker-compose.yml
└── README.md
```

## Database Models

### User
```python
{
  "id": int,
  "firebase_uid": string,
  "name": string,
  "email": string,
  "password": string (nullable),
  "plan": string (default: "FREE")
}
```

### Chat
```python
{
  "id": int,
  "user": int (FK),
  "title": string
}
```

### Message
```python
{
  "id": int,
  "chat": int (FK),
  "sender": string ("user" or "chatbot"),
  "content": text,
  "date": datetime
}
```

## Security

- **Firebase Authentication**: JWT tokens issued by Firebase
- **API Gateway**: Validates JWT tokens before routing requests
- **Protected Routes**: All endpoints except `/auth/signup/` and `/auth/signin/` require authentication
- **Service Account Keys**: Never commit `serviceAccountKey.json` to version control

## Monitoring

- **Eureka Dashboard**: http://localhost:8888
- **Spring Boot Actuator**: Enabled on API Gateway

## Troubleshooting

### Service not registering with Eureka
- Ensure Eureka server is running
- Check network connectivity between services
- Verify `eureka.client.service-url.defaultZone` in configuration

### Authentication fails
- Verify Firebase service account key is properly configured
- Check JWT token format (must be `Bearer <token>`)
- Ensure token hasn't expired

### Database connection issues
- Verify PostgreSQL is running
- Check database credentials in environment variables
- Ensure database exists: `mydb`

### Docker container issues
```bash
# View logs
docker-compose logs -f [service-name]

# Rebuild containers
docker-compose down
docker-compose up --build

# Remove volumes
docker-compose down -v
```

## Development

### Adding a new microservice

1. Create service with Spring Boot or Django
2. Register with Eureka
3. Add route in `gateway-api/src/main/resources/application.yml`
4. Add service to `docker-compose.yml`

### Running tests

#### Spring Boot services
```bash
./mvnw test
```

#### Django service
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue in the repository.
