# Social Backend API

A Django backend API for a social platform that enables user registration, authentication, friend requests, and friend management.

## Features

- User registration with email/password or Google authentication
- JWT-based authentication
- User profile management
- Friend requests (send, accept, reject)
- Friend listing
- Friend suggestions
- Search functionality
- Pagination for list endpoints

## Tech Stack

- **Framework**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Hmtgit7/social-backend-api.git
   cd python-backend
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

5. Run database migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login to get JWT token
- `POST /api/auth/google/` - Login with Google
- `POST /api/auth/refresh/` - Refresh JWT token

### User Profile
- `GET /api/users/me/` - Get current user profile
- `PATCH /api/users/me/` - Update user profile

### User Management
- `GET /api/users/` - List all users (except self)
- `GET /api/users/?search=query` - Search users by name

### Friend Management
- `GET /api/friends/suggestions/` - Get friend suggestions
- `GET /api/friends/` - List all friends
- `GET /api/friends/requests/` - List friend requests (incoming and outgoing)
- `POST /api/friends/requests/{user_id}/` - Send friend request
- `PUT /api/friends/requests/{request_id}/accept/` - Accept friend request
- `PUT /api/friends/requests/{request_id}/reject/` - Reject friend request

## Testing

Run the test suite:
```bash
pytest
```

## Postman Collection

A Postman collection is included in the `postman` directory for easy API testing.

## License

[MIT](LICENSE)