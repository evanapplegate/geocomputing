# All Res Full Res

Social media app for sharing high-resolution images with ar.en.a-inspired minimal design.

## Features

- Google SSO authentication
- Image storage in Cloudflare R2
- Two-image posts (50% viewport width each)
- Auto-appended "download full res" links
- User profiles with avatars and custom links (Twitter, Instagram, Website)
- Password reset flow
- Email change functionality

## Setup

### Quick local sandbox (no SSO keys)

1. **Backend**
   - Copy `backend/.env.example` to `backend/.env`
   - Set `ALLOW_MOCK_AUTH=true`
   - Leave the OAuth/Cloudflare variables blank (the backend will automatically switch to SQLite + local file storage under `backend/local_media`)
2. **Frontend**
   - Copy `frontend/.env.example` to `frontend/.env`
   - Set `VITE_ENABLE_MOCK_AUTH=true` to reveal the “Dev login” button
3. Run the backend and frontend dev servers as described below, then click “Dev login (local)” on the landing page to get an auth token and start uploading files (stored locally via `/local-media`).

### Backend

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables (copy `.env.example` to `.env` and fill in values)

3. Set up database:
```bash
alembic upgrade head
```

4. Run server:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run dev server:
```bash
npm run dev
```

## Deployment

### Heroku

1. Create Heroku app and add Postgres addon
2. Set environment variables in Heroku dashboard
3. Deploy:
```bash
git push heroku main
heroku run alembic upgrade head
```

## Environment Variables

See `backend/.env.example` and `frontend/.env.example` for required variables. When deploying, ensure `ALLOW_MOCK_AUTH` and `VITE_ENABLE_MOCK_AUTH` remain `false`.
