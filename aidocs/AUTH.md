# Authentication Implementation for Advertising Dashboard MVP

## Overview

This document outlines the authentication implementation for the Advertising Dashboard MVP using Streamlit and in-memory storage. Since Streamlit doesn't provide built-in authentication, we'll implement a custom solution that integrates with our data models and in-memory data store.

## User Authentication Flow

1. **Login/Registration Screen** - Initial page shown to unauthenticated users
2. **Session-based Authentication** - Using Streamlit's session state to maintain login status
3. **Password Handling** - Secure password hashing and verification
4. **Access Control** - Route protection for authenticated pages

## Technical Implementation

### In-Memory Storage

- **User Store Implementation**:
  - Python dictionary with user records keyed by user ID
  - Secondary indices for username and email lookups
  - Based on UserSchema from MODEL.md

  ```python
  # Example in-memory user store structure
  users_by_id = {}
  users_by_username = {}
  users_by_email = {}
  ```

- **User Record Structure**:
  - `id` (UUID4): Primary key
  - `username`: Unique username
  - `email`: Unique email address
  - `password_hash`: Securely hashed password with salt
  - `created_at`: Account creation timestamp
  - `last_login`: Last login timestamp

### Key Components

#### 1. Password Security

- PBKDF2 with SHA-256 algorithm for password hashing
- Unique salt per password
- 100,000 iterations for computational security

#### 2. User Registration Process

- Validate input data against UserSchema
- Check for existing users with same username/email
- Hash password with salt
- Generate UUID4 for user ID
- Store user record in memory

#### 3. User Authentication Process

- Retrieve user record by username
- Verify provided password against stored hash
- Update last login timestamp
- Return user data and authentication status
- Store authenticated state in Streamlit session

#### 4. Streamlit Session Management

- Use Streamlit's session_state to maintain authentication status
- Store user data in session for authenticated users
- Provide login, registration, and logout functionality
- Create authentication check mechanism for protected routes

## Application Structure

### Unauthenticated State

- Login tab with username/password form
- Registration tab with new user creation form
- Both tabs accessible without authentication

### Authenticated State

- Welcome message with username in sidebar
- Logout button in sidebar
- Access to protected dashboard features
- Automatic redirect to authenticated content

## Security Considerations

1. **Password Hashing** - Using PBKDF2 with SHA-256 for secure password storage
2. **Input Validation** - All user inputs are validated through Pydantic
3. **Session Management** - Using Streamlit's session state for secure session handling
4. **Memory Limits** - Set reasonable limits on user accounts for the MVP

## Mock Authentication Option

For testing and demonstration purposes, a mock authentication mode can be enabled that:

- Creates predefined test users at startup
- Allows for quick testing without registration
- Can be toggled on/off as needed

Example implementation:

```python
def initialize_mock_users():
    """Create mock users for testing"""
    from datetime import datetime
    import uuid
    from passlib.hash import pbkdf2_sha256

    mock_users = [
        {
            "id": str(uuid.uuid4()),
            "username": "demo",
            "email": "demo@example.com",
            "password_hash": pbkdf2_sha256.hash("password"),
            "created_at": datetime.now(),
            "last_login": None
        },
        {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": pbkdf2_sha256.hash("admin"),
            "created_at": datetime.now(),
            "last_login": None
        }
    ]

    # Add to in-memory store
    for user in mock_users:
        users_by_id[user["id"]] = user
        users_by_username[user["username"]] = user
        users_by_email[user["email"]] = user
```

This authentication implementation provides a secure, user-friendly solution that meets the requirements of the Advertising Dashboard MVP while leveraging the data models defined in MODEL.md and in-memory storage for simplicity and rapid development.
