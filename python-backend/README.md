# Social Backend API - Django Implementation

A Django REST API for a social platform with user authentication, profile management, and friend functionality.

## Features

- **User Authentication:**
  - Email/Password registration and login
  - Google OAuth authentication
  - JWT-based authentication with refresh tokens

- **User Management:**
  - Get and update user profile
  - List all users
  - Search users by name

- **Friend System:**
  - Send friend requests
  - Accept/reject friend requests
  - List friends
  - Get friend suggestions

## Tech Stack

- **Backend Framework:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Testing:** pytest

## Prerequisites

- Python 3.9+
- PostgreSQL (v12 or higher)
- pip and virtualenv

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Hmtgit7/social-backend-api.git
cd social-backend-api/python-backend
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file with the following variables:

```bash
# Django settings
DEBUG=True
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=social_api
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# JWT settings
JWT_SECRET_KEY=your_jwt_secret
JWT_ACCESS_TOKEN_LIFETIME=1h
JWT_REFRESH_TOKEN_LIFETIME=7d

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

5. **Set up the database:**

Create a PostgreSQL database:

```bash
psql -U postgres -c "CREATE DATABASE social_api;"
```

Apply migrations:

```bash
python manage.py migrate
```

6. **Create a superuser (admin):**

```bash
python manage.py createsuperuser
```

## Running the Application

Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

The admin interface will be available at `http://localhost:8000/admin/`.

## API Endpoints

### Authentication

- **Register a new user:**
  - `POST /api/auth/register/`
  - Request body: `{ "name": "John Doe", "email": "john@example.com", "password": "password123" }`

- **Login a user:**
  - `POST /api/auth/login/`
  - Request body: `{ "email": "john@example.com", "password": "password123" }`
  - Returns: Access and refresh tokens

- **Refresh JWT token:**
  - `POST /api/auth/refresh/`
  - Request body: `{ "refresh": "your_refresh_token" }`

- **Google Authentication:**
  - `POST /api/auth/google/`
  - Request body: `{ "token": "google-id-token" }`

### User Management

- **Get current user profile:**
  - `GET /api/users/me/`
  - Authentication: Required (JWT Token)

- **Update current user profile:**
  - `PATCH /api/users/me/`
  - Authentication: Required (JWT Token)
  - Request body: `{ "name": "Updated Name", "bio": "Updated bio" }`

- **List all users (except self):**
  - `GET /api/users/`
  - Authentication: Required (JWT Token)
  - Query parameters: `page` (default: 1), `page_size` (default: 10)

- **Search users by name:**
  - `GET /api/users/?search=John`
  - Authentication: Required (JWT Token)
  - Query parameters: `search`, `page`, `page_size`

### Friend Management

- **Send friend request:**
  - `POST /api/friends/requests/{user_id}/`
  - Authentication: Required (JWT Token)

- **Accept friend request:**
  - `PUT /api/friends/requests/{request_id}/accept/`
  - Authentication: Required (JWT Token)

- **Reject friend request:**
  - `PUT /api/friends/requests/{request_id}/reject/`
  - Authentication: Required (JWT Token)

- **List friends:**
  - `GET /api/friends/`
  - Authentication: Required (JWT Token)
  - Query parameters: `page`, `page_size`

- **List friend requests:**
  - `GET /api/friends/requests/`
  - Authentication: Required (JWT Token)
  - Returns both received and sent requests

- **Get friend suggestions:**
  - `GET /api/friends/suggestions/`
  - Authentication: Required (JWT Token)

## Authentication Flow

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer your_jwt_token
```

## Project Structure

```
python-backend/
├── accounts/              # User authentication and profiles
│   ├── models.py          # User model
│   ├── serializers.py     # Serialization for User objects
│   ├── views.py           # User API views
│   └── urls.py            # User API URLs
├── friends/               # Friend functionality
│   ├── models.py          # Friend request model
│   ├── serializers.py     # Serialization for friend objects
│   ├── views.py           # Friend API views
│   └── urls.py            # Friend API URLs
├── social_backend/        # Main project directory
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── tests/                 # Test directory
├── .env                   # Environment variables
├── .env.example           # Example environment variables
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Testing

Run the test suite:

```bash
pytest
```

## API Testing with Postman

A Postman collection is included in the `postman` directory for easy testing of the API endpoints.

### How to use the Postman collection:

1. Import the `postman/Social_API.postman_collection.json` file into Postman
2. Set the environment variable `baseUrl` to `http://localhost:8000/api` (or your custom URL)
3. Execute the "Register User" request first to get authentication tokens
4. Other requests will automatically use the access token

## Example cURL Requests

### Register a user:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe", 
    "email": "john@example.com", 
    "password": "password123"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get user profile:
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Bonus Features

- Comprehensive test coverage
- Search functionality to find users by name
- Pagination for listing endpoints
- Proper error handling
- JWT refresh tokens

## License

MIT