# 🏏 Cricketer Tracker API

A full-featured **FastAPI** application to manage cricketers, teams, and match performance data — ideal for learning, sports apps, or fantasy cricket engines. Built with FastAPI, SQLModel, and SQLite.

---

## 🚀 Features

- 👤 Manage **Superuser**: Create, view, and assign superusers to manage the deletion and creation of every managed data
- 👤 Manage **Adminstrator**: Create, view, and assign administrators to manage the deletion and creation
- 👤 Manage **Cricketers**: Create, view, and assign players to teams
- 🧢 Manage **Teams**: Track cricket teams and their countries
- 📈 Log **Match Performances**: Track runs, wickets, match types, and opponents
- 🔒 Clean project structure using FastAPI and SQLModel
- 🧪 Generates **dummy data** at startup for easy testing
- 🗃️ SQLite for simple and lightweight storage
- 📦 Modular architecture: `models`, `schemas`, `crud`, `routers`, `db`

---

## 📁 Project Structure

<pre>
cricketer_tracker_api/  
├── db/ │  
│       └── session.py # Database connection & session setup  
├── models/ │  
│           ├──superuser.py #Superuser SQLModel
│           ├──admin.py #Administrator SQLModel
│           ├── cricketer.py # Cricketer SQLModel  
│           ├── team.py # Team SQLModel  
│           └── performance.py # Match performance SQLModel  
├── schemas/ │  
│            ├──superuser.py # Pydantic schemas for superuser 
│            ├──admin.py # Pydantic schemas for Admin
│            ├── cricketer.py # Pydantic schemas for Cricketer  
│            ├── team.py # Pydantic schemas for Team  
│            └── performance.py # Pydantic schemas for MatchPerformance  
├── crud/ │  
│         ├──superuser.py # DB logic for superuser
│         ├──admin.py # DB logic for admin
│         ├── cricketer.py # DB logic for cricketers  
│         ├── team.py # DB logic for teams  
│         └── performance.py # DB logic for performances  
├── routers/ │  
│            ├──superuser.py # Superuser endpoints
│            ├──admin.py # Admin endpoints
│            ├── cricketer.py # Cricketer endpoints  
│            ├── team.py # Team endpoints  
│            └── performance.py # MatchPerformance endpoints  
├── main.py # FastAPI entry point  
├── dummy_data.txt # Generated dummy login data  
├── requirements.txt # Dependencies  
└── README.md
</pre>

---

## 🧪 Dummy Data

- Dummy teams, cricketers, and match performances are created at startup
- Ensures consistent test data is available
- You can customize the number of records in each generator function
- Logs usernames and passwords (if applicable) to `dummy_admin_superuser.txt`

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/cricketer_tracker_api.git
cd cricketer_tracker_api
```

---

## Set up virtual environment

python -m venv venv  
venv\Scripts\activate # On Windows  
source venv/bin/activate # On Linux/macOS

---

## Install dependencies

pip install -r requirements.txt

---

## 4. Run the server (using FastAPI CLI or Uvicorn)

From project root directory

fastapi dev --app CRICKETER_TRACKER_API.main:app --reload

OR

uvicorn CRICKETER_TRACKER_API.main:app --reload

---

## 🧠 API Endpoints

| Method | Endpoint                  | Description                |
| ------ | ------------------------- | -------------------------- |
| GET    | `/superuser/get_all`      | Get all superusers         |
| POST   | `/superuser/register`     | Create a superuser         |
| GET    | `/administrator/get_all`  | Get all administrators     |
| POST   | `/administrator/register` | Create a administrator     |
| GET    | `/cricketers/get_all`     | Get all cricketers         |
| POST   | `/cricketers/register`    | Create a cricketer         |
| GET    | `/teams/get_all`          | Get all teams              |
| POST   | `/teams/register`         | Create a team              |
| GET    | `/performances/get_all`   | Get all match performances |
| POST   | `/performances/register`  | Log new match performance  |

You can explore all endpoints via the auto-generated docs:

- Swagger UI: http://localhost:8000/docs or https://cricketertracker-jt74vllod-muhammad-mutayyab-hafeezs-projects.vercel.app/docs (Deployed using vercel)

- ReDoc: http://localhost:8000/redoc or https://cricketertracker-jt74vllod-muhammad-mutayyab-hafeezs-projects.vercel.app/redoc (Deployed using vercel)

---

## 💡 Tech Stack

- FastAPI 🚀

- SQLModel

- SQLite

- Faker for dummy data

- Pydantic v2 (from_attributes=True for schemas)

---

## 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first.
