# 📋 Todo List App

A simple web system for registering and managing a list of todos.

## 🧱 Technologies

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Frontend**: [React](https://react.dev/)
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Monorepo**: Backend and frontend are in the same repository

---

## 🚀 How to Run the Project

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11 installed locally (for user creation script)

### Steps

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Make the startup script executable:

```bash
chmod +x start.sh
```

3. Start the application stack:
 ```bash
 ./start.sh
```

This will start:

* FastAPI backend at http://localhost:8000
* React frontend at http://localhost:3000
* PostgreSQL (inside the container)


👤 Create Admin User
After the containers are up, you need to manually create a user to log into the system.

1. Access the backend container:
```bash
docker exec -it backend bash
```

2. Run the user creation script:
```bash
python3 scripts/create_user.py
```
This script will create a default user with credentials defined in the script (username and password).


🛠 Features
* User login
* Todo CRUD operations
* JWT-based authentication (backend)
* Full integration between frontend and backend

🗂 Project Structure

```bash
.
├── backend
│   ├── main.py
│   ├── models.py
│   ├── crud.py
│   ├── database.py
│   ├── auth.py
│   ├── auth_token.py
│   ├── auth_middleware.py
│   ├── init_db.py
│   ├── schemas.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── scripts/
│       └── create_user.py
├── frontend
│   ├── Dockerfile
│   └── src/
│       └── (React components)
├── docker-compose.yml
├── start.sh
└── README.md
```

✅ To Do
* Add user registration page
* Improve UI with CSS/Tailwind
* Add search and filters

Made with 💻 by Daniel Gallo.
