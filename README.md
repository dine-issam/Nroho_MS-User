# Microservices Chat Application

A microservices-based chat application built with Spring Boot (Gateway API) and Django (User Microservice), featuring Firebase authentication and Eureka service discovery.

## Architecture Overview

```
┌─────────────────┐
│  Eureka Server  │
│   (Port 8888)   │
└────────┬────────┘
         │
         ├──────────────────────────┐
         │                          │
┌────────▼─────────┐       ┌────────▼──────────┐
│   Gateway API    │       │    ms-user        │
│  (Port 7777)     │◄──────┤   (Port 8000)     │
│  Spring Boot     │       │    Django         │
│  + Firebase Auth │       │  + PostgreSQL     │
└──────────────────┘       └───────────────────┘
```

## Components

### 1. Eureka Server (Service Discovery)
- **Port:** 8888
- **Purpose:** Service registry for microservices communication
- **URL:** `http://localhost:8888/eureka`

### 2. Gateway API (Spring Boot)
- **Port:** 7777
- **Framework:** Spring Boot 3.5.6 with Spring Cloud Gateway
- **Java Version:** 21
- **Authentication:** Firebase JWT Token verification
- **Features:**
  - API Gateway and routing
  - Firebase authentication filter
  - Eureka client for service discovery
  - Routes requests to microservices

**Key Dependencies:**
- Spring Cloud Gateway
- Spring Security
- Firebase Admin SDK
- Netflix Eureka Client

### 3. ms-user (Django Microservice)
- **Port:** 8000
- **Framework:** Django 5.2.6 with Django REST Framework
- **Database:** PostgreSQL
- **Features:**
  - User management with Firebase integration
  - Chat and message functionality
  - Eureka client registration

**Models:**
- **User**: Stores user information with Firebase UID
- **Chat**: Chat sessions associated with users
- **Message**: Individual messages within chats

## Prerequisites

- **Java:** JDK 21
- **Python:** 3.8+
- **PostgreSQL:** Latest version
- **Maven:** 3.9.11 (via wrapper)
- **Firebase:** Project with Admin SDK credentials

## Setup Instructions

### 1. Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Email/Password authentication
3. Download the service account key JSON file
4. Place the file in:
   - Gateway API: `gateway-api/src/main/resources/serviceAccountKey.json`
   - Django: `ms_user/ms_user/serviceAccountKey.json`

### 2. PostgreSQL Database Setup

```bash
# Create database
createdb ms_user-db

# Or using psql
psql -U postgres
CREATE DATABASE "ms_user-db";
```

### 3. Gateway API Setup

```bash
cd gateway-api

# Configure application.yml (update IP addresses)
# Edit: src/main/resources/application.yml
# Set your machine's LAN IP for eureka.instance.hostname

# Run the application
./mvnw spring-boot:run
```

**Configuration (`application.yml`):**
```yaml
server:
  port: 7777

eureka:
  instance:
    hostname: 172.20.10.3  # Replace with your LAN IP
```

### 4. Django ms-user Setup

```bash
cd ms_user

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=your-django-secret-key
FIREBASE_API_KEY=your-firebase-web-api-key
EOF

# Configure Eureka client
# Edit: userapp/eureka_client.py
# Set INSTANCE_HOST to your LAN IP

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver 0.0.0.0:8000
```

**Environment Variables:**
- `SECRET_KEY`: Django secret key
- `FIREBASE_API_KEY`: Firebase Web API key
- `PG_USER`: PostgreSQL username (default: postgres)
- `PG_PASSWORD`: PostgreSQL password (default: mysecretpassword)
- `PG_DB`: Database name (default: ms_user-db)
- `PG_PORT`: Database port (default: 5432)
- `PG_HOST`: Database host (default: localhost)

## API Endpoints

All requests through Gateway API should include the Firebase ID token in headers:
```
Authorization: Bearer <firebase-id-token>
```

### Authentication (Public - No Token Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ms-user/auth/signup/` | Register new user |
| POST | `/ms-user/auth/signin/` | Login user |

**Signup Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "plan": "FREE"
}
```

**Signin Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Signin Response:**
```json
{
  "user": {
    "id": 1,
    "firebase_uid": "...",
    "email": "user@example.com",
    "name": "John Doe",
    "plan": "FREE"
  },
  "idToken": "eyJhbGciOiJSUzI1...",
  "refreshToken": "..."
}
```

### Users (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ms-user/users/` | List all users |
| GET | `/ms-user/users/{id}/` | Get user by ID |
| POST | `/ms-user/users/create/` | Create user |
| PUT | `/ms-user/users/update/{id}/` | Update user |
| DELETE | `/ms-user/users/delete/{id}/` | Delete user |

### Chats (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ms-user/chats/` | List all chats |
| GET | `/ms-user/chats/{id}/` | Get chat by ID |
| POST | `/ms-user/chats/create/` | Create chat |
| PUT | `/ms-user/chats/update/{id}/` | Update chat |
| DELETE | `/ms-user/chats/delete/{id}/` | Delete chat |

**Create Chat Request:**
```json
{
  "user": 1,
  "title": "My Chat Session"
}
```

### Messages (Protected)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ms-user/messages/` | List all messages |
| GET | `/ms-user/messages/chat/{chat_id}/` | Get messages by chat |
| GET | `/ms-user/messages/{id}/` | Get message by ID |
| POST | `/ms-user/messages/create/` | Create message |
| PUT | `/ms-user/messages/update/{id}/` | Update message |
| DELETE | `/ms-user/messages/delete/{id}/` | Delete message |

**Create Message Request:**
```json
{
  "chat": 1,
  "sender": "user",
  "content": "Hello, how can I help you?"
}
```

## Security

### Gateway API Security
- JWT verification using Firebase Admin SDK
- Only `/ms-user/auth/signup/` and `/ms-user/auth/signin/` are public
- All other endpoints require valid Firebase ID token
- Stateless authentication (no session storage)

### Django Security
- Firebase Auth middleware validates tokens
- Database password hashing
- CSRF protection enabled
- Secure database connections

## Service Discovery Flow

1. **Eureka Server** starts on port 8888
2. **Gateway API** registers with Eureka as `api-gateway`
3. **ms-user** registers with Eureka as `ms-user`
4. Gateway routes requests to microservices using service names
5. Load balancing handled by Spring Cloud Gateway

## Development

### Running Locally

1. Start Eureka Server (separate project not included)
2. Start PostgreSQL database
3. Start Gateway API: `./mvnw spring-boot:run`
4. Start Django ms-user: `python manage.py runserver`

### Network Configuration

Both services use LAN IP addresses for inter-service communication. Update the following:

**Gateway API** (`application.yml`):
```yaml
eureka:
  instance:
    hostname: YOUR_LAN_IP
```

**Django** (`userapp/eureka_client.py`):
```python
INSTANCE_HOST = "YOUR_LAN_IP"
EUREKA_SERVER = "http://YOUR_LAN_IP:8888/eureka"
```

## Testing

### Test Authentication Flow

```bash
# 1. Signup
curl -X POST http://localhost:7777/ms-user/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'

# 2. Signin
curl -X POST http://localhost:7777/ms-user/auth/signin/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 3. Use the returned idToken for authenticated requests
curl -X GET http://localhost:7777/ms-user/users/ \
  -H "Authorization: Bearer YOUR_ID_TOKEN"
```

## Troubleshooting

### Common Issues

**1. Service not registering with Eureka**
- Verify network connectivity
- Check LAN IP addresses are correct
- Ensure Eureka server is running

**2. Authentication failures**
- Verify Firebase credentials are correctly placed
- Check token expiration
- Ensure Firebase project settings are correct

**3. Database connection errors**
- Verify PostgreSQL is running
- Check database credentials
- Ensure database exists

**4. Port conflicts**
- Gateway: 7777
- Django: 8000
- Eureka: 8888
- PostgreSQL: 5432

## Technology Stack

- **Backend Gateway:** Spring Boot, Spring Cloud Gateway, Spring Security
- **Backend Microservice:** Django, Django REST Framework
- **Authentication:** Firebase Authentication
- **Service Discovery:** Netflix Eureka
- **Database:** PostgreSQL
- **API Documentation:** SpringDoc OpenAPI (Gateway)

## License

This project is for intership at Nroho.

## Contributors

Developed as a microservices architecture demonstration project.
