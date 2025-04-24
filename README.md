# Social Backend API

This repository contains implementations of a social platform backend API in both Node.js/Express and Python/Django, along with a React frontend.

## Repository Structure

```
social-backend-api/
├── node-backend/     # Express.js implementation
├── python-backend/   # Django implementation
└── react-frontend/   # React frontend (coming soon)
```

## Feature Overview

Both backend implementations provide the following features:

- User registration & authentication (email/password and Google OAuth)
- JWT-based authentication
- User profile management
- Friend requests (send, accept, reject)
- Friend listing
- Friend suggestions
- User search
- Pagination for list endpoints

## Technology Stack

### Node.js Backend
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Authentication**: JWT with Passport.js
- **Testing**: Jest

### Python Backend
- **Framework**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest

## Getting Started

Choose which backend implementation you want to use and follow the setup instructions:

- [Node.js Backend Setup](#nodejs-backend-setup)
- [Python Backend Setup](#python-backend-setup)

## Node.js Backend Setup

### Prerequisites
- Node.js 16+ and npm
- PostgreSQL

### Setup Instructions

1. Navigate to the Node.js backend directory:
   ```bash
   cd node-backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

4. Set up the database:
   ```bash
   # Create the database
   psql -U postgres -c "CREATE DATABASE social_api;"
   
   # Initialize the database schema
   node scripts/init-db.js
   ```
   
   Note: The `init-db.js` script reads the SQL commands from `db/init.sql` and executes them to set up your database tables and indexes.

5. Start the server:
   ```bash
   npm run dev
   ```

6. The API will be available at: `http://localhost:3000/api`

## Python Backend Setup

### Prerequisites
- Python 3.9+
- PostgreSQL

### Setup Instructions

1. Navigate to the Python backend directory:
   ```bash
   cd python-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration values
   ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. The API will be available at: `http://localhost:8000/api`

## API Documentation

Both backends implement the same API endpoints with slight variations in URL structure.

### Node.js Backend API Endpoints

#### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login to get JWT token
- `POST /api/auth/google` - Login with Google

#### User Profile
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile

#### User Management
- `GET /api/users` - List all users (except self)
- `GET /api/users/search?name=query` - Search users by name

#### Friend Management
- `GET /api/friends/suggestions` - Get friend suggestions
- `GET /api/friends` - List all friends
- `GET /api/friends/requests` - List friend requests
- `POST /api/friends/request` - Send friend request
- `PUT /api/friends/request/:requestId` - Accept/reject friend request

### Python Backend API Endpoints

#### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login to get JWT token
- `POST /api/auth/google/` - Login with Google
- `POST /api/auth/refresh/` - Refresh JWT token

#### User Profile
- `GET /api/users/me/` - Get current user profile
- `PATCH /api/users/me/` - Update user profile

#### User Management
- `GET /api/users/` - List all users (except self)
- `GET /api/users/?search=query` - Search users by name

#### Friend Management
- `GET /api/friends/suggestions/` - Get friend suggestions
- `GET /api/friends/` - List all friends
- `GET /api/friends/requests/` - List friend requests
- `POST /api/friends/requests/{user_id}/` - Send friend request
- `PUT /api/friends/requests/{request_id}/accept/` - Accept friend request
- `PUT /api/friends/requests/{request_id}/reject/` - Reject friend request

## Testing the API

### Postman Collections

Postman collections are provided for testing both backend implementations:

- Node.js Backend: `node-backend/Social_API.postman_collection.json`
- Python Backend: `python-backend/postman/Social_API.postman_collection.json`

### Running Tests

#### Node.js Backend
```bash
cd node-backend
npm test
```

#### Python Backend
```bash
cd python-backend
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.