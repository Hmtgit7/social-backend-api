# Social Backend API - Node.js Implementation

A RESTful API for a social platform with user authentication, profile management, and friend functionality.

## Features

- **User Authentication:**
  - Email/Password registration and login
  - Google OAuth authentication
  - JWT-based authentication

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

- **Backend:** Node.js, Express.js
- **Database:** PostgreSQL
- **Authentication:** JWT, Passport.js, Google OAuth
- **Validation:** Express Validator

## Prerequisites

- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)
- npm or yarn

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Hmtgit7/social-backend-api.git
cd social-backend-api/node-backend
```

2. **Install dependencies:**

```bash
npm install
```

3. **Set up environment variables:**

Create a `.env` file with the following variables:

```bash
# Server Configuration
PORT=3000
NODE_ENV=development

# Database Configuration
DB_USER=postgres
DB_HOST=localhost
DB_NAME=social_api
DB_PASSWORD=your_password
DB_PORT=5432

# JWT Configuration
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRES_IN=7d

# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

4. **Set up the database:**

Create a PostgreSQL database:

```bash
psql -U postgres -c "CREATE DATABASE social_api;"
```

Initialize the database schema:

```bash
node scripts/init-db.js
```

This script will use the SQL commands in `db/init.sql` to set up your tables and indexes.

## Running the Application

Start the server in development mode:

```bash
npm run dev
```

Or in production mode:

```bash
npm start
```

The server will start running at `http://localhost:3000/api` (or the port specified in your `.env` file).

## API Endpoints

### Authentication

- **Register a new user:**
  - `POST /api/auth/register`
  - Request body: `{ "name": "John Doe", "email": "john@example.com", "password": "password123" }`

- **Login a user:**
  - `POST /api/auth/login`
  - Request body: `{ "email": "john@example.com", "password": "password123" }`

- **Google Authentication:**
  - `POST /api/auth/google`
  - Request body: `{ "token": "google-id-token" }`

### User Management

- **Get current user profile:**
  - `GET /api/users/me`
  - Authentication: Required (JWT Token)

- **Update current user profile:**
  - `PUT /api/users/me`
  - Authentication: Required (JWT Token)
  - Request body: `{ "name": "Updated Name", "bio": "Updated bio" }`

- **List all users (except self):**
  - `GET /api/users`
  - Authentication: Required (JWT Token)
  - Query parameters: `page` (default: 1), `limit` (default: 10)

- **Search users by name:**
  - `GET /api/users/search?name=John`
  - Authentication: Required (JWT Token)
  - Query parameters: `name`, `page` (default: 1), `limit` (default: 10)

- **Get user by ID:**
  - `GET /api/users/:id`
  - Authentication: Required (JWT Token)

### Friend Management

- **Send friend request:**
  - `POST /api/friends/request`
  - Authentication: Required (JWT Token)
  - Request body: `{ "userId": 123 }`

- **Respond to friend request:**
  - `PUT /api/friends/request/:requestId`
  - Authentication: Required (JWT Token)
  - Request body: `{ "action": "accept" }` or `{ "action": "reject" }`

- **List friends:**
  - `GET /api/friends`
  - Authentication: Required (JWT Token)
  - Query parameters: `page` (default: 1), `limit` (default: 10)

- **List friend requests:**
  - `GET /api/friends/requests`
  - Authentication: Required (JWT Token)

- **Get friend suggestions:**
  - `GET /api/friends/suggestions`
  - Authentication: Required (JWT Token)

## Authentication Flow

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer your_jwt_token
```

## Testing

Run the test suite:

```bash
npm test
```

## API Testing with Postman

A Postman collection is included for easy testing of the API endpoints.

### How to use the Postman collection:

1. Import the `Social_API.postman_collection.json` file into Postman
2. Set the environment variable `baseUrl` to `http://localhost:3000/api` (or your custom URL)
3. Execute the "Register User" request first to get an authentication token
4. Other requests will automatically use this token

## Example cURL Requests

### Register a user:
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Login:
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Get user profile:
```bash
curl -X GET http://localhost:3000/api/users/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Project Structure

```
node-backend/
├── src/
│   ├── config/              # Configuration files
│   ├── controllers/         # Request handlers
│   ├── middleware/          # Custom middleware
│   ├── models/              # Database models
│   ├── routes/              # API routes
│   ├── utils/               # Helper functions
│   ├── validators/          # Input validation schemas
│   └── app.js              # Express app setup
├── db/
│   └── init.sql            # Database initialization SQL
├── scripts/
│   └── init-db.js          # Database initialization script
├── tests/                  # Unit tests
├── .env                    # Environment variables
├── .env.example            # Example environment variables
├── package.json            # Project dependencies
└── server.js               # Entry point
```

## Bonus Features

- Search functionality to find users by name
- Pagination for listing endpoints
- Comprehensive validation and error handling
- Google OAuth authentication

## License

MIT