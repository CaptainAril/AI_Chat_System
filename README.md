
# AI Chat System API

## Description
This is the backend API for the AI Chat System, providing basic operations such as user signup, login, JWT-based authentication, user token balance checks, chat message handling, and user logout. The system allows users to interact with an AI-powered chatbot. The chatbot provides responses to user queries and deducts tokens from the user's account for each question asked.

---

## Python Version
- Python 3.12.3

## Installation and Run Commands
To run the API locally, clone the `AI_Chat_System` repository and set up a virtual environment.

### Set up and Run Virtual Environment
In the repository's root directory, run:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies in Virtual Environment
```bash
pip install -r requirements.txt
```

## Setup and Execution
### Django Startup
Create and apply migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Development Notes

- This project is set up with `sqlite` as the default database; you may need to adjust `DATABASES` in `settings.py` if you wish to switch to another database.



Start the Django server:
```bash
python3 manage.py runserver
```

The server will be running at `http://127.0.0.1:8000/`. Use this URL with the following endpoints to test the API.

---

## Endpoints and Usage

### Users

#### 1. `api/v1/users/`
* **POST** – Creates a new user account.
    * **Request Data**:
        - `username`: Account username.
        - `password`: Account password.
    * **Usage**:
        ```bash
        curl -X POST http://127.0.0.1:8000/api/v1/users/ -H 'Content-Type: application/json' -d '{"username": "<username>", "password": "<password>"}'
        ```
    * **Response**:
        - **Success**: `201 Created` – `{"status": "successs", "message":"User Account created", 'data':{"username": "<username>", "token": "<integer>" }}`  - token => 4000 default value
        - **Failure**: `400 Bad Request` – `{"status": "An Error occured", "error": "Username already exists" }`

#### 2. `api/v1/users/all/` *(Authentication Required)*
* **GET** – Retrieve the list of all active users.
    * **Usage**:
        ```bash
        curl -X GET http://127.0.0.1:8000/api/v1/users/all/ -H "Authorization: Bearer <token>"
        ```
    * **Response**:
        - **Success**: `200 OK` – `{'message' : 'All Users retrieved', 'status': 'success', 'data': [{"username": "<username1>" }, { "username": "<username2>" }]}`
        - **Failure**: `401 Unauthorized` – `{ "detail": "Authentication credentials were not provided." }`

#### 3. `api/v1/users/login/`
* **POST** – Logs in and authenticates a user.
    * **Request Data**:
        - `username`: Account username.
        - `password`: Account password.
    * **Usage**:
        ```bash
        curl -X POST http://127.0.0.1:8000/api/v1/users/login/ -H 'Content-Type: application/json' -d '{"username": "<username>", "password": "<password>"}'
        ```
    * **Response**:
        - **Success**: `200 OK` – `{"status":"200", "message":"Login succesful", "username": "<username>", "access": "<jwt_access_token>", "refresh": "<jwt_refresh_token>" }`
        - **Failure**: `401 Unauthorized` – `{"status": "401", "message": "Invalid Credentials" }`

#### 4. `api/v1/users/logout/` *(Authentication Required)*
* **POST** – Logs out user and blacklists refresh token.
    * **Request Data**:
        - `refresh`: Refresh token.
    * **Usage**:
        ```bash
        curl -X POST http://127.0.0.1:8000/api/v1/users/logout/ -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' -d '{"refresh": "<refresh_token>"}'
        ```
    * **Response**:
        - **Success**: `200 OK` – `{"status":"success", "message": "Logged out successfully" }`
        - **Failure**: 
                - `401 Unauthorized` – `{ "detail": "Authentication credentials were not provided." }`
                - `400 Bad Request` – `{"status": "error", "message": "Invalid or expired refresh token"}`

#### 5. `api/v1/users/token-balance/` *(Authentication Required)*
* **GET** – Retrieves the token balance of the logged-in user.
    * **Usage**:
        ```bash
        curl -X GET http://127.0.0.1:8000/api/v1/users/token-balance/ -H "Authorization: Bearer <token>"
        ```
    * **Response**:
        - **Success**: `200 OK` – `{"status":"success", "message":"Token balance", "username": "<username>", "token_balance": <integer> }`
        - **Failure**: `401 Unauthorized` – `{ "detail": "Authentication credentials were not provided." }`

---

### Chat

#### 1. `api/v1/chats/` *(Authentication Required)*
* **POST** – Sends a message to the chat API and deducts tokens.
    * **Request Data**:
        - `message`: The message from the user.
    * **Usage**:
        ```bash
        curl -X POST http://127.0.0.1:8000/api/v1/chats/ -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' -d '{"message": "<user_message>"}'
        ```
    * **Response**:
        - **Success**: `200 OK` – `{"status":"success", "message":"New Chats record", "user_account":"<username>", "chat":{"message":"<user_message>","response":"<AI_response>","timestamp":"<message_timestamp>"}}`
        - **Failure**:
            - `401 Unauthorized` – `{ "detail": "Authentication credentials were not provided." }`
            - `402 Payment Required` – `{"status": "error", "message": "Insufficient tokens" }`

---

### Refresh Token

#### 6. `api/v1/token/refresh/`
* **POST** – Refreshes the access token using a valid refresh token.
    * **Request Data**:
        - `refresh`: A valid refresh token.
    * **Usage**:
        ```bash
        curl -X POST http://127.0.0.1:8000/api/v1/users/refresh/ -H 'Content-Type: application/json' -d '{"refresh": "<refresh_token>"}'
        ```
    * **Response**:
        - **Success**: `200 OK` – `{ "access": "<new_access_token>", "refresh": "<new_refresh_token>" }`
        - **Failure**:
            - `401 Unauthorized` – `{ "detail":"Token is invalid or expired", "code":"token_not_valid" }`
            - `400 Bad Request` – `{ "error": "Refresh token is required" }`

---


### Notes

- **Authentication**: Endpoints marked with *(Authentication Required)* require a valid JWT access token in the `Authorization` header.
- **Error Handling**: Each endpoint is designed to return appropriate HTTP status codes for successful and failed requests.
- **Token Expiry**: Tokens expire based on the settings in `SIMPLE_JWT`, with access tokens lasting 6 minutes and refresh tokens lasting 30 minutes.

---

