# Stream Interaction Dashboard

This project is a full-stack web application for visualizing live stream session data, statistics, and viewer trends. It consists of a **React frontend** and a **Flask backend** connected to a **PostgreSQL database**.

## 🚀 Features
- View **stream sessions** with platform and streamer details.
- Display **stream statistics** (followers gained, gifts, top commenter, etc.).
- Show **viewer trends** using dynamic charts.
- Fetch live data from **PostgreSQL** via a **Flask API**.

---

## 📂 Project Structure
```
/stream-interaction
├── /frontend   (React app - UI)
│   ├── /src
│   │   ├── /components  (UI components)
│   │   ├── /pages  (Dashboard page)
│   │   ├── App.js
│   │   ├── index.js
│   ├── package.json
│   ├── README.md
├── /backend    (Flask app - API & Database)
│   ├── app.py  (Flask server)
│   ├── db.py   (PostgreSQL connection)
│   ├── .env    (Environment variables)
│   ├── requirements.txt
└── README.md
```

---

## 🛠️ Setup & Installation


### **2️⃣ Set Up the Backend (Flask + PostgreSQL)**
#### **Install Python Dependencies**
```sh
cd backend
python -m venv venv  # Create virtual environment
source venv/bin/activate  # Activate (Mac/Linux)
venv\Scripts\activate  # Activate (Windows)
pip install -r requirements.txt  # Install dependencies
```

#### **Set Up Environment Variables**
Create a `.env` file inside `backend/` and add:
```
DB_NAME=streaming_analytics
DB_USER=postgres
DB_PASS=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

#### **Run Database Migrations**
Make sure PostgreSQL is running, then execute:
```sh
python db.py  # Creates tables if they don't exist
```

#### **Start the Flask API**
```sh
python app.py  # Runs on http://127.0.0.1:5000
```

---

### **3️⃣ Set Up the Frontend (React + TailwindCSS)**
#### **Install Node.js & npm (if not installed)**
Check if Node.js is installed:
```sh
node -v
npm -v
```

#### **Install Frontend Dependencies**
```sh
cd frontend
npm install
```

#### **Start the React Development Server**
```sh
npm start  # Runs on http://localhost:3000
```

---

## 🚀 Running the Application
### **Backend (Flask)**
- Ensure **PostgreSQL is running**.
- Run `python app.py` in the **backend** folder.

### **Frontend (React)**
- Run `npm start` in the **frontend** folder.
- Open `http://localhost:3000` in your browser.

---

## 🛠️ API Endpoints
| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| GET    | `/api/sessions`        | Get all stream sessions |
| GET    | `/api/stats`           | Get stats for all sessions |
| GET    | `/api/viewers/:id`     | Get viewer count for a session |

---

## ✅ Troubleshooting
### **CORS Error (Frontend can't access Backend)**
- Ensure Flask has **CORS enabled** in `app.py`:
  ```python
  from flask_cors import CORS
  CORS(app)
  ```

### **PostgreSQL Connection Error**
- Ensure PostgreSQL is running.
- Check `.env` file for correct database credentials.
- Try connecting manually:
  ```sh
  psql -U postgres -d streaming_analytics
  ```

### **Port Conflicts**
- If Flask (5000) or React (3000) ports are in use, change them in:
  - **Flask**: `app.run(port=5001)`
  - **React**: `package.json` (`start` script -> `PORT=3001 react-scripts start`)

---

## 🎯 Next Steps
- **Deploy the app** to **Heroku (Flask)** & **Vercel (React)**.
- **Enhance UI** with **filters & real-time updates**.
- **Add authentication** (e.g., JWT, OAuth).

---

🚀 **Enjoy your Stream Interaction Dashboard!** 🚀

