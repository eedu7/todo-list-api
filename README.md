# Todo List API
Sample solution for the [todo-list-api](https://roadmap.sh/projects/todo-list-api) challenge from [roadmap.sh](https://roadmap.sh/).

## How to run

```bash
$ git clone https://github.com/eedu7/todo-list-api.git
$ cd todo-list-api
$ pip install -r requirements.txt
$ python main.py
```

# Given below is a list of the endpoints and the details of the request and response:

## User Registration
Register a new user using the following request:

```POST /register```
```json
{
  "name": "John Doe",
  "email": "john@doe.com"
  "password": "password"
}
```
This will validate the given details, make sure the email is unique and store the user details in the database. Make sure to hash the password before storing it in the database. Respond with a token that can be used for authentication if the registration is successful.
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}
```
The token can either be a JWT token or a random string that can be used for authentication. We leave it up to you to decide the implementation details.

## User Login
Authenticate the user using the following request:

```POST /login```
```json
{
  "email": "john@doe.com",
  "password": "password"
}
```
This will validate the given email and password, and respond with a token if the authentication is successful.
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}
```
## Create a To-Do Item
Create a new to-do item using the following request:

```POST /todos```
```json
{
  "title": "Buy groceries",
  "description": "Buy milk, eggs, and bread"
}
```
User must send the token received from the login endpoint in the header to authenticate the request. You can use the Authorization header with the token as the value. In case the token is missing or invalid, respond with an error and status code 401.
```json
{
  "message": "Unauthorized"
}
```
Upon successful creation of the to-do item, respond with the details of the created item.
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Buy milk, eggs, and bread"
}
```
## Update a To-Do Item
Update an existing to-do item using the following request:

```PUT /todos/1```

```json
{
  "title": "Buy groceries",
  "description": "Buy milk, eggs, bread, and cheese"
}
```
Just like the create todo endpoint, user must send the token received. Also make sure to validate the user has the permission to update the to-do item i.e. the user is the creator of todo item that they are updating. Respond with an error and status code 403 if the user is not authorized to update the item.
```json
{
  "message": "Forbidden"
}
```
Upon successful update of the to-do item, respond with the updated details of the item.
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Buy milk, eggs, bread, and cheese"
}
```
### Delete a To-Do Item
Delete an existing to-do item using the following request:

```DELETE /todos/1```
User must be authenticated and authorized to delete the to-do item. Upon successful deletion, respond with the status code 204.

### Get To-Do Items
Get the list of to-do items using the following request:

```GET /todos?page=1&limit=10```
User must be authenticated to access the tasks and the response should be paginated. Respond with the list of to-do items along with the pagination details.
```json
{
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Buy milk, eggs, bread"
    },
    {
      "id": 2,
      "title": "Pay bills",
      "description": "Pay electricity and water bills"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 2
}
```
