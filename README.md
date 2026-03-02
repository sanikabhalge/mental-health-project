# MindCare Backend – Auth (JWT + SQLite)

FastAPI backend with **JWT auth** and **SQLite**. Users are stored in `mindcare.db`; login/register return an **access token** you send in the `Authorization` header for protected routes.

---

## 1. How to run

### One-time setup

```bash
cd backend
python -m venv venv
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Swagger docs: http://localhost:8000/docs  

The first time you run, SQLite will create `mindcare.db` in the `backend` folder with a `users` table.

---

## 2. How to use the API

### Register (sign up)

**Request:**
```http
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "username": "john",
  "password": "secret123",
  "age": 25,
  "gender": "male",
  "emergencyContact": "Jane 9876543210",
  "phoneNumber": "9876543210",
  "address": "123 Main St"
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john",
    "created_at": "2025-02-01T12:00:00"
  }
}
```

### Login

**Request:**
```http
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "john",
  "password": "secret123"
}
```

**Response (200):** Same shape as register – `access_token`, `token_type`, `user`.

### Using the JWT (protected routes later)

For any protected endpoint, send the token in the header:

```http
Authorization: Bearer <access_token>
```

Example with curl after login:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8000/api/some-protected-route
```

The backend has a `get_current_user` dependency you can use: `Depends(get_current_user)` – it will read the JWT and return the logged-in user.

---

## 3. Run frontend + backend together

1. **Terminal 1 – backend:**
   ```bash
   cd backend
   venv\Scripts\activate   # or source venv/bin/activate
   uvicorn main:app --reload --port 8000
   ```

2. **Terminal 2 – frontend:**
   ```bash
   cd frontend/client
   npm install
   npm run dev
   ```

3. Open http://localhost:5173 – use **Login** or **Sign Up**. The frontend will call the backend and store the JWT in `localStorage`; after login/signup you’re taken to the chat page.

---

## 4. Optional: environment variables

Create a `.env` file in the `backend` folder to override defaults:

```env
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///./mindcare.db
```

- `SECRET_KEY` – used to sign JWTs; change in production.  
- `DATABASE_URL` – default is SQLite; you can switch to PostgreSQL later with a URL like `postgresql://user:pass@localhost/mindcare`.
