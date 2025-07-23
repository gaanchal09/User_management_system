## User Management System
A simple, thread-safe User Management REST API for handling user CRUD operations and migration of "messy" data. This project uses Python and Flask, ideal for learning about APIs, migrations, and backend structure.

## Features

- **User CRUD API:** Create, read, update, delete users via HTTP endpoints.
- **Migration support:** Script/logic to import and clean up "messy" user data.
- **Thread-safe storage:** Uses locks to prevent data corruption.
- **Error handling:** Manages incomplete or invalid records gracefully.
- **Automated tests:** Includes tests for main endpoints and edge cases.

## Getting Started

### Prerequisites

```bash
- Python 3.8 or higher  
- pip (Python package installer)
```
### Installation

Clone the repository:
```bash
git clone https://github.com/your_username/messy-migration.git
cd messy-migration
```

Install dependencies:
```pip install -r requirements.txt
```

## Running the Application

Initialize the database/data storage (if required):
```python init_db.py
```


Start the API server:
```python app.py
```


The API will run at: http://localhost:5000/

## API Endpoints

| Method | Endpoint        | Description            | Request Body Example     |
| ------ | --------------- | ---------------------- | ----------------------- |
| POST   | `/users`        | Create user            | `{ "name": "Alice" }`   |
| GET    | `/users`        | List all users         |                         |
| GET    | `/users/<id>`   | Get user by ID         |                         |
| PUT    | `/users/<id>`   | Update user            | `{ "name": "Bob" }`     |
| DELETE | `/users/<id>`   | Delete user            |                         |
| POST   | `/migrate`      | Migrate messy user data| `[ { user objects… } ]` |

### Example: Creating a User

```
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"Alice"}'
```

## Data Migration

Use the `/migrate` endpoint or the provided migration script to import existing user data that may be incomplete or "messy."

The migration process will:  
- Validate each record  
- Skip or transform malformed entries  
- Ensure the integrity and consistency of the new user dataset

## Running Tests

Execute automated tests with:

```
pytest
```


## Project Structure

messy-migration/
│
├── app.py # Main API server
├── models.py # User storage and thread-safety
├── migration.py # Migration logic/scripts
├── test_basic.py # Automated tests
├── requirements.txt # Dependencies
└── README.md # Documentation (this file)

