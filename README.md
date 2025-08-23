# Key-Value Store with Transactions

A Python-based Key-Value Store with transaction support, built with Flask and SQLite.

## How to Run

### 1. Setup

```bash
cd /path/to/Arcade-Take-Home
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Server

Run this in the terminal:

```bash
python -c "
from backend.kv_api.app import create_app
app = create_app()
app.run(host='0.0.0.0', port=8000, debug=True)
"
```

Server runs at: **http://localhost:8000**

### 3. Test API

```bash
# Store data
curl -X PUT http://localhost:8000/put/kv/test \
  -H "Content-Type: application/json" \
  -d '{"value": "hello world"}'

# Get data
curl http://localhost:8000/get/kv/test

# Update data
curl -X UPDATE http://localhost:8000/update/kv/test \
  -H "Content-Type: application/json" \
  -d '{"value": "updated value"}'

# Delete data
curl -X DELETE http://localhost:8000/delete/kv/test
```

### 4. Example Session

```bash
# Store user data
curl -X PUT http://localhost:8000/put/kv/test_user \


# Update the user
curl -X UPDATE http://localhost:8000/update/kv/test_user \


# Get updated data
curl http://localhost:8000/get/kv/test_user

# Delete the user
curl -X DELETE http://localhost:8000/delete/kv/test_user

# Verify deletion
curl http://localhost:8000/get/kv/test_user


```

### 5. Run Tests

```bash
pip install pytest pytest-flask
pytest tests/test_api.py -v
```

### 6. Troubleshooting

If we get database lock errors, restart with a clean database:

```bash
# Stop the Flask server (Ctrl+C)
rm -f kv_store.db
# Restart the server
source venv/bin/activate && python -c "
from backend.kv_api.app import create_app
app = create_app()
app.run(host='0.0.0.0', port=8000, debug=True)
"
```

## API Endpoints

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| PUT    | `/put/kv/<key>`    | Store a key-value pair  |
| GET    | `/get/kv/<key>`    | Retrieve a value by key |
| UPDATE | `/update/kv/<key>` | Update existing key     |
| DELETE | `/delete/kv/<key>` | Delete a key-value pair |

## Design Decisions

### Database Schema

- **Keys as TEXT**: Chose performance over flexibility - string keys cover 99% of use cases
- **Values as BLOB**: Used pickle serialization to meet "store anything" requirement
- **No transaction_id column**: SQLite handles transactions natively - avoid reinventing the wheel

### Architecture Choices

- **Three-layer separation**: Flask → Transactions → DatabaseManager for clean separation of concerns
- **Pending operations pattern**: Queue operations by type `{"set": [], "update": [], "delete": []}`
- **State flag approach**: Same API methods work for both immediate and transactional operations

### Technology Decisions

- **SQLite over complex databases**: Built-in, zero-config, perfect for requirements
- **File-based storage**: Real persistence requirement - data survives server restarts
- **Sync over async**: Prioritized working software over optimization given time constraints
- **Custom exceptions**: Single `KVStoreError` class provides consistent error reporting

**Philosophy**: Chose simplicity and functionality over complex optimizations.
