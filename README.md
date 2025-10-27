# 🌙 Moon Robot Control API

A FastAPI backend for controlling a lunar exploration robot with obstacle detection and position tracking.

## 🚀 Quick Start

**Start the entire application with one command:**

```bash
docker-compose up --build
```

The API will be available at: **http://localhost:8000**

This automatically:
- Starts PostgreSQL database
- Runs database migrations
- Initializes obstacles
- Starts the FastAPI server

## 📖 API Usage

### Get Robot Position

```bash
curl http://localhost:8000/api/v1/robot/position
```

**Response:**
```json
{
  "x": 4,
  "y": 2,
  "direction": "WEST"
}
```

### Execute Commands

```bash
curl -X POST http://localhost:8000/api/v1/robot/commands \
  -H "Content-Type: application/json" \
  -d '{"commands": "FLFFFRFLB"}'
```

**Response:**
```json
{
  "x": 2,
  "y": 0,
  "direction": "SOUTH",
  "commands_executed": "FLFFFRFLB",
  "stopped_by_obstacle": false,
  "obstacle_coordinate": null
}
```

### Commands

- `F` - Move forward
- `B` - Move backward  
- `L` - Turn left
- `R` - Turn right

### Test Obstacle Detection

```bash
# Move to position (4, 4)
curl -X POST http://localhost:8000/api/v1/robot/commands \
  -H "Content-Type: application/json" \
  -d '{"commands": "RFF"}'

# Try to move west - will hit obstacle at (1, 4)
curl -X POST http://localhost:8000/api/v1/robot/commands \
  -H "Content-Type: application/json" \
  -d '{"commands": "LFFFF"}'
```

**Response:**
```json
{
  "x": 2,
  "y": 4,
  "direction": "WEST",
  "commands_executed": "LFFFF",
  "stopped_by_obstacle": true,
  "obstacle_coordinate": [1, 4]
}
```

### API Documentation

- **Swagger UI**: http://localhost:8000/docs

## 🧪 Running Tests

```bash
# Install test dependencies
poetry add --group dev aiosqlite

# Run all tests
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=app

# Run specific test file
poetry run pytest tests/test_obstacles.py -v
```

**Note:** Tests use SQLite in-memory (no PostgreSQL required for testing!)

## ⚙️ Configuration

Edit `.env` to customize:

```bash
START_POSITION_X=4
START_POSITION_Y=2
START_DIRECTION=WEST
OBSTACLES=1,4;3,5;7,4
```

## 🛠️ Local Development (Optional)

If you prefer to run locally without Docker:

```bash
# Install dependencies
poetry install

# Start PostgreSQL only
docker-compose up -d postgres

# Run migrations
poetry run alembic upgrade head

# Start API
poetry run uvicorn app.main:app --reload
```

## 📊 Project Structure

```
moon-robot-api/
├── app/
│   ├── api/v1/routes/      # API endpoints
│   ├── services/           # Business logic
│   ├── repositories/       # Data access
│   ├── db/models/          # Database models
│   └── main.py             # FastAPI app
├── tests/                  # Test suite
├── alembic/                # Database migrations
├── docker-compose.yml      # Docker setup
└── Dockerfile              # API container
```

## 🏗️ Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Alembic** - Migrations
- **Docker** - Containerization
- **pytest** - Testing

## 🎯 Features

✅ Robot position tracking  
✅ Command execution (F, B, L, R)  
✅ Obstacle detection  
✅ Command history  
✅ Environment configuration  
✅ Auto-migrations  
✅ Comprehensive tests  
✅ Liniting, formatting and sorting of imports (using black, ruff, mypy and Isort)

---

**By: Muhammad Talha Ghaffar for Exmox (m.talhaghaffar07@gmail.com) 🌙🤖