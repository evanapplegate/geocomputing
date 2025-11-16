# Meta Prompt: All Res Full Res - Social Media App

## Project Overview
Build a social media application called "All Res Full Res" with a design aesthetic similar to ar.en.a. The app allows users to share images with captions and provides full-resolution downloads.

## Core Requirements

### Authentication & User Management
- **Google SSO**: Implement OAuth 2.0 Google Sign-In
  - Use `google-auth` and `google-auth-oauthlib` libraries
  - Store user tokens securely (encrypted in database)
  - Session management with secure cookies
- **User Profile Features**:
  - Avatar upload (store in Cloudflare R2 bucket)
  - Display name (editable)
  - Email address (with change email functionality)
  - Password reset flow (email-based with secure tokens, 24hr expiry)
  - Three customizable links:
    - Link 1: Twitter/X (default label "Twitter")
    - Link 2: Instagram (default label "Instagram") 
    - Link 3: Personal site (default label "Website")
    - Links are optional, editable, and displayed on user profile

### Image Storage & Delivery
- **Cloudflare R2 Bucket**:
  - Store all user-uploaded images
  - Generate public URLs for image serving
  - Implement image optimization/compression for thumbnails
  - Full-resolution images stored separately from display versions
  - Use Cloudflare R2 SDK (`boto3` with R2 endpoint or `cloudflare` SDK)
- **Image Processing**:
  - Accept common formats: JPEG, PNG, WebP
  - Generate optimized display versions (max 1920px width, quality 85%)
  - Preserve original full-resolution files
  - Store metadata: original filename, upload date, dimensions, file size

### Hosting: Heroku
- **Deployment Configuration**:
  - `Procfile` with gunicorn/uvicorn for production server
  - `requirements.txt` with all dependencies pinned
  - `runtime.txt` specifying Python version (3.11+)
  - Environment variables for:
    - Database URL (PostgreSQL)
    - Cloudflare R2 credentials (access key, secret key, bucket name, endpoint)
    - Google OAuth credentials (client ID, client secret)
    - Secret key for session encryption
    - Email service credentials (SendGrid/Mailgun for password reset)
- **Database**: PostgreSQL (Heroku Postgres addon)
  - User table: id, email, google_id, display_name, avatar_url, password_hash (nullable), created_at, updated_at
  - UserLinks table: id, user_id, link_type (twitter/instagram/website), url, created_at
  - Post table: id, user_id, image_url_full, image_url_display, caption, created_at, updated_at
  - PasswordResetToken table: id, user_id, token (hashed), expires_at, used

### UI/UX Design

#### Layout Structure
- **Two-column image display**:
  - Each image takes 50% viewport width (`50vw`)
  - Images maintain aspect ratio
  - Responsive: stacks vertically on mobile (< 768px)
  - Images are clickable/expandable for full view
- **Post Component**:
  - Two images side-by-side (or stacked on mobile)
  - Caption text below images
  - Auto-appended link at end of caption: "download full res" → links to full-resolution image
  - Link styling: subtle underline, hover effect
- **Design Aesthetic** (ar.en.a inspired):
  - Minimal, clean typography
  - Generous white space
  - Monochrome or muted color palette
  - Sans-serif font (Inter, Helvetica Neue, or similar)
  - Subtle shadows/borders
  - Smooth transitions/animations

#### Pages/Routes
1. **Home Feed** (`/`):
   - Grid/list of posts (two images per post)
   - Infinite scroll or pagination
   - Post author name/avatar links to profile
2. **User Profile** (`/user/:username`):
   - User avatar, display name
   - Three custom links (if set)
   - Grid of user's posts
   - Edit profile button (if own profile)
3. **Upload Post** (`/upload`):
   - Two image upload fields
   - Caption textarea
   - Preview before posting
   - Upload progress indicator
4. **Settings** (`/settings`):
   - Change display name
   - Upload/change avatar
   - Change email (with verification)
   - Set/edit three custom links
   - Password reset option
5. **Login/Signup** (`/auth/google`):
   - Google OAuth flow
   - Redirect handling

### Technical Stack

#### Backend (Python)
- **Framework**: FastAPI or Flask
  - FastAPI recommended for async/await support with R2 uploads
- **Database ORM**: SQLAlchemy (with Alembic for migrations)
- **Authentication**: `python-jose` for JWT tokens, `passlib` for password hashing
- **File Upload**: `python-multipart` for form handling
- **Image Processing**: `Pillow` (PIL) for image optimization
- **HTTP Client**: `httpx` or `requests` for R2 API calls

#### Frontend
- **Framework**: React (or Next.js for SSR)
  - Component structure:
    - `PostCard` component (two images + caption)
    - `UserProfile` component
    - `ImageUpload` component
    - `LinkEditor` component (for profile links)
- **Styling**: CSS Modules or Tailwind CSS
  - Mobile-first responsive design
  - CSS Grid/Flexbox for layout
- **State Management**: React Context or Zustand
- **HTTP Client**: `axios` or `fetch` API

### API Endpoints

```
POST   /api/auth/google          # Initiate Google OAuth
GET    /api/auth/callback        # OAuth callback handler
POST   /api/auth/logout          # Logout user
GET    /api/user/me              # Get current user
PUT    /api/user/me              # Update user profile
POST   /api/user/avatar          # Upload avatar
PUT    /api/user/links           # Update profile links
POST   /api/auth/reset-password  # Request password reset
POST   /api/auth/reset-password/:token # Complete password reset
PUT    /api/user/email           # Change email (with verification)

GET    /api/posts                # Get feed (paginated)
POST   /api/posts                # Create new post
GET    /api/posts/:id            # Get single post
DELETE /api/posts/:id            # Delete post (author only)
GET    /api/users/:username      # Get user profile
GET    /api/users/:username/posts # Get user's posts
```

### Implementation Details

#### Image Upload Flow
1. User selects two images via file input
2. Frontend validates: file type, size (< 50MB each), dimensions
3. Frontend sends to backend `/api/posts` with multipart/form-data
4. Backend:
   - Validates files
   - Generates unique filenames (UUID + extension)
   - Uploads full-res to R2: `posts/{user_id}/{post_id}/full/{filename}`
   - Processes display version (resize, compress)
   - Uploads display version to R2: `posts/{user_id}/{post_id}/display/{filename}`
   - Stores URLs in database
   - Returns post object with image URLs

#### Caption with Auto-Appended Link
- Caption stored as plain text in database
- Frontend renders caption, then appends: ` [download full res]`
- Link points to: `/api/posts/:id/download` or direct R2 URL (signed URL for security)
- Styling: link appears inline, same font size, subtle color difference

#### Password Reset Flow
1. User requests reset via `/api/auth/reset-password` (provides email)
2. Backend generates secure token (32 chars, URL-safe)
3. Hash token and store in PasswordResetToken table (expires 24hr)
4. Send email with link: `https://app.com/reset-password/:token`
5. User clicks link, enters new password
6. Backend validates token, updates password, marks token as used
7. User redirected to login

#### Email Change Flow
1. User submits new email via `/api/user/email`
2. Backend sends verification email to new address
3. User clicks verification link
4. Backend updates email, sends confirmation to old email

### Security Considerations
- All user inputs sanitized (prevent XSS)
- CSRF protection on state-changing endpoints
- Rate limiting on auth endpoints (prevent brute force)
- Image upload validation (file type, size limits)
- Signed URLs for R2 downloads (expire after 1 hour)
- Password hashing with bcrypt (cost factor 12)
- JWT tokens expire after 7 days, refresh tokens after 30 days
- HTTPS only (enforced by Heroku)

### Environment Variables Template
```bash
DATABASE_URL=postgresql://...
CLOUDFLARE_R2_ACCESS_KEY_ID=...
CLOUDFLARE_R2_SECRET_ACCESS_KEY=...
CLOUDFLARE_R2_BUCKET_NAME=all-res-full-res
CLOUDFLARE_R2_ENDPOINT=https://...
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
SECRET_KEY=... # For session encryption
EMAIL_API_KEY=... # SendGrid/Mailgun
EMAIL_FROM=noreply@allresfullres.com
FRONTEND_URL=https://allresfullres.herokuapp.com
```

### Database Schema (SQLAlchemy Models)

```python
class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    google_id = Column(String, unique=True, nullable=True)
    display_name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)  # For email/password users
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class UserLink(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    link_type = Column(String, nullable=False)  # 'twitter', 'instagram', 'website'
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url_full_1 = Column(String, nullable=False)
    image_url_display_1 = Column(String, nullable=False)
    image_url_full_2 = Column(String, nullable=False)
    image_url_display_2 = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class PasswordResetToken(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
```

### Testing Checklist
- [ ] Google SSO login works
- [ ] Image upload to R2 succeeds
- [ ] Display images load correctly
- [ ] Full-res download link works
- [ ] Password reset email sends and link works
- [ ] Email change verification works
- [ ] Profile links save and display
- [ ] Avatar upload works
- [ ] Two-column layout responsive on mobile
- [ ] Caption auto-appends "download full res" link
- [ ] Posts display in feed chronologically
- [ ] User profiles show correct posts

### Deployment Steps
1. Create Heroku app: `heroku create all-res-full-res`
2. Add Postgres addon: `heroku addons:create heroku-postgresql:mini`
3. Set environment variables via Heroku dashboard
4. Initialize database: `alembic upgrade head`
5. Deploy: `git push heroku main`
6. Run migrations: `heroku run alembic upgrade head`
7. Verify: Check logs `heroku logs --tail`

### Performance Optimizations
- Image lazy loading on frontend
- Database indexes on user_id, created_at
- CDN caching for display images (Cloudflare)
- Pagination for feed (20 posts per page)
- Async image processing (Celery/background tasks if needed)

---

**Success Criteria**: App allows users to sign in with Google, upload two images with captions, view feed of posts, access full-resolution downloads, manage profile with avatar and links, and reset passwords. All images stored in Cloudflare R2, served via Heroku, with ar.en.a-inspired minimal design.
