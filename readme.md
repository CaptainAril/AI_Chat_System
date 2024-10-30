# AI CHAT SYSTEM

# Description
This provide the GiveHope API that server the GiveHope platform. Basic API operations include creation of causes, donaion requests, making donations, users signup, login, authentication and authorization

------

## Python version
- 3.12.3
# Installation and run commands
- Clone the `AI_Chat_System` repository into your local machine to be able to run the API
## Set up and run Virtual Environment
In the repo's root directory, run the following commands:
- `python3 -m venv .venv`
- `source .venv/bin/activate`
## Install Dependencies in virtual env
- `pip3 install -r requirements.txt`

# Setup and execution
## Django startup

Make models migrations and migrate to database
- `python3 manage.py makemigrations`
- `python3 manage.py migrate`

Note: This project utilizes sqlite database

Spin the Django server
- `python3 manage.py runserver`

This start a django server at `http://127.0.0.1:8000/`.

Use this url, along with the endpoints to test the API.


## Endpoints And Usage
### Users
- api/v1/users/

    * POST – Creates a new user account.
        * Required data:
            - username: Account username.
            - password: Account password.

        - Usage: curl -X POST http://127.0.0.1:8000/api/v1/users/ -H 'Content-Type: application/json' -d '{username=`<username>`, password=`<password>`}'
    ***

- api/v1/users/all/
    * GET – Retrieve the list of all active users.
        - Usage: curl -X GET http://127.0.0.1:8000/api/v1/users/all/
    ***


- api/v1/users/login/
    * POST – Logs in and authenticates a user
        * Required data:
            - username: Account username.
            - password: Account password.
        - Usage: curl -X POST http://127.0.0.1:8000/api/v1/users/login/ -H 'Content-Type: application/json' -d '{username=`<username>`, password=`<password>`}'

    ***
- api/users/logout/
    * POST – Logs out user and blacklist's refresh token
        * Required data:
            - refresh: refresh token
            - password: Account password.
        - Usage: curl -X POST http://127.0.0.1:8000/api/v1/users/logout/ -H 'Content-Type: application/json' -d '{refresh=`<refresh_token>`}'
    ***

- api/v1/users/token-balance/
    * GET – Retrieves the details of the current logged in user.
        - Usage: curl -X GET http://127.0.0.1:8000/- api/v1/users/token-balance/ -H "Cookie: sessionid=`<your_session_id>`"

### Chat
- api/v1/chats/     -  `authenticated`
    * POST – creates a new cause
        * Required data:
            - message: message from user.

        - Usage: curl -X POST http://127.0.0.1:8000/api/v1/chats/ -H 'Content-Type: application/json' -d '{message=`<message>`}'
    ***
- api/causes/``<str:title>``/
    * GET – retrieve the cause with specified title
        - Usage: curl -X GET http://127.0.0.1:8000/api/causes/`<title>`/

    * PUT – Updataes the cause with specified title
        - Usage: curl -X PUT http://127.0.0.1:8000/api/causes/`<title>`/ -H 'Content-Type: application/json' -d '{`<updated_data>`}'

    * DELETE – Deletes the cause with specified title
        - Usage: curl -X DELETE http://127.0.0.1:8000/api/causes/`<title>`/



Please note that the ``<str:title>`` in the URL should be replaced with the actual title of the cause you want to retrieve, update, or delete.

Remember to replace `<your_session_id>`, `<first_name>`, `<last_name>`, `<email>`, `<password>`, `<confirm_password>`, `<nationality>`, `<phone_number>`, `<address>`, `<state_city>`, `<gender>`, `<zip_code>`, `<name>`, `<organization_desc>`, `<organization_number>`, `<website>`, `<address>`, `<updated_data>`, and `<title>` with the appropriate values in the requests.

    ***

You can use these endpoints to interact with the GiveHope API from the frontend application. Make sure to handle authentication, error handling, and validation on the frontend side as per application's requirements.
