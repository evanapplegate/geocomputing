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

See `backend/.env.example` for required variables.
