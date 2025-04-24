What this Application Does
This is a social media backend API with the following core functionalities:

User Authentication System

User registration with email/password
Login with JWT tokens
Google authentication (optional)
Custom user profiles


User Management

View and update user profiles
List other users
Search for users by name


Friend Management

Send friend requests
Accept/reject friend requests
List your current friends
Get friend suggestions



Testing with Postman
Let's set up a Postman collection to test all the endpoints. I'll provide the request details and sample data for each endpoint.
Setting up Postman

Open Postman and create a new collection called "Social Backend API"
Create a new environment and add the following variables:

base_url: http://127.0.0.1:8000
token: (leave empty for now)



Endpoints to Test
1. User Registration

Method: POST
URL: {{base_url}}/api/auth/register/
Body (raw JSON):

json{
  "email": "user1@example.com",
  "name": "Test User",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}

Response: Should return a user object, access token, and refresh token.
Post-request Script (to save token):

javascriptif (pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access);
}
2. User Login

Method: POST
URL: {{base_url}}/api/auth/login/
Body (raw JSON):

json{
  "email": "user1@example.com",
  "password": "securepassword123"
}

Response: Should return user data and tokens.
Post-request Script:

javascriptif (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("token", jsonData.access);
}
3. Get User Profile

Method: GET
URL: {{base_url}}/api/users/me/
Headers:

Authorization: Bearer {{token}}


Response: Should return the authenticated user's profile.

4. Update User Profile

Method: PATCH
URL: {{base_url}}/api/users/me/
Headers:

Authorization: Bearer {{token}}


Body (raw JSON):

json{
  "name": "Updated Name",
  "bio": "This is my updated bio",
  "profile_picture": "https://example.com/profile.jpg"
}

Response: Should return the updated profile.

5. List All Users

Method: GET
URL: {{base_url}}/api/users/
Headers:

Authorization: Bearer {{token}}


Response: Should return a list of all users except the authenticated one.

6. Search Users

Method: GET
URL: {{base_url}}/api/users/?search=test
Headers:

Authorization: Bearer {{token}}


Response: Should return users matching the search term.

7. Create Additional Test Users
Create 3-4 more users to test friend functionality:

Method: POST
URL: {{base_url}}/api/auth/register/
Body Examples:

json{
  "email": "user2@example.com",
  "name": "User Two",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
8. Send Friend Request

Method: POST
URL: {{base_url}}/api/friends/requests/2/
Headers:

Authorization: Bearer {{token}}


Response: Should return the created friend request.
Note: Replace "2" with the actual user ID you want to send a request to.

9. List Friend Requests

Method: GET
URL: {{base_url}}/api/friends/requests/
Headers:

Authorization: Bearer {{token}}


Response: Should return all incoming and outgoing friend requests.

10. Accept Friend Request

Method: PUT
URL: {{base_url}}/api/friends/requests/1/accept/
Headers:

Authorization: Bearer {{token}}


Response: Should confirm the request was accepted.
Note: Replace "1" with the actual request ID you want to accept.

11. Reject Friend Request

Method: PUT
URL: {{base_url}}/api/friends/requests/2/reject/
Headers:

Authorization: Bearer {{token}}


Response: Should confirm the request was rejected.
Note: Replace "2" with the actual request ID you want to reject.

12. List Friends

Method: GET
URL: {{base_url}}/api/friends/
Headers:

Authorization: Bearer {{token}}


Response: Should return a list of your friends.

13. Get Friend Suggestions

Method: GET
URL: {{base_url}}/api/friends/suggestions/
Headers:

Authorization: Bearer {{token}}


Response: Should return suggested users to befriend.

Additional Notes

Admin Access: You can use the superuser you created (abc@gmail.com) to log in to the admin panel at http://127.0.0.1:8000/admin/
Database Content: When testing friend requests, pay attention to the IDs of users and requests in your database.
JWT Tokens: The tokens expire after some time (usually 1 hour for access tokens), so you might need to log in again if you encounter 401 errors.

Checking Implementation Against Requirements
Let's confirm that our implementation meets all the specified requirements:

User Registration & Authentication ✅

Registration with email/password works
JWT-based login implemented
Basic validations in place


Get User Profile ✅

Authenticated users can view their profile
Profile updating works


List All Users (Except Self) ✅

API endpoint returns other users


Friend Suggestions ✅

Random user suggestions implemented


Send Friend Request ✅

Users can send requests to others


Accept/Reject Friend Request ✅

Handling of request statuses works


List Friends ✅

Shows accepted friendships


BONUS Features ✅

Search functionality implemented
Pagination for listing endpoints
Tests for major endpoints