# FastAPI JWT + Storage

Minimal FastAPI app with JWT auth (signup/login) and an in-memory storage API. Interactive docs available in Swagger UI.


## Run

Create .env:

```text
JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_M=30
HOST=0.0.0.0
PORT=8080
```

Start server:

```bash
uv run app/main.py
```


## Usage

### Auth

- POST /auth/signup

- POST /auth/login

### Storage

- POST /storage/add_record

- POST /storage/change_record

- DELETE /storage/delete_record

- GET /storage/get_record

### Debug

- DELETE /debug/delete_user

- GET /debug/get_all_users

- GET /debug/get_all_records
