# Meta Prompt V2: All Res Full Res - Enhanced Requirements

## Design Updates

### Typography
- Font stack: `'Optima', -apple-system, BlinkMacSystemFont, 'Verdana', sans-serif`
- Apply globally across all components

### Image Requirements
- **Minimum file size**: 10MB per image
- **Supported formats**: PNG, JPG, TIFF, RAW (CR2, NEF, ARW, etc.)
- **Validation**: Reject images smaller than 10MB
- **Upload interface**: Large, prominent drop zone with clear messaging

## Landing Page

### ASCII Art Header
Generate ASCII art for "All Res Full Res" - bold, centered, prominent

### Authentication Options
- Google SSO button (existing)
- GitHub SSO button (new - implement OAuth)
- Both buttons styled consistently, prominent on landing page

### Post-Registration Flow
After user registers/logs in:
1. Show large drop zone interface
2. Text: "drop at least 1x 10mb image here [PNG/JPG/TIFF/RAW]"
3. Drag-and-drop functionality
4. File validation (size + format)
5. Upload progress indicator

## Navigation Structure

### Two-Tab Layout
Top navigation with two tabs:
1. **My Posts**: Shows user's own posts (timeline)
2. **My Feed**: Shows feed of all users' posts

### Tab Behavior
- Active tab highlighted
- Smooth transitions
- Maintain state when switching tabs

## Post Flow

### Upload Process
1. User drops/uploads image(s)
2. Validate: minimum 10MB, supported format
3. Optional caption field
4. Upload to R2 (full-res only, no compression)
5. Post appears immediately in "My Posts" tab
6. Post appears in "My Feed" for all users

## Backend Updates

### GitHub OAuth
- Add GitHub OAuth integration
- Store `github_id` in User model
- Similar flow to Google OAuth

### Image Validation
- Enforce 10MB minimum on backend
- Support RAW formats (check MIME types or extensions)
- Store original files without compression

### API Endpoints
- `GET /api/posts/my` - Get current user's posts
- `GET /api/posts/feed` - Get feed (all posts)
- Update upload to handle single large image (10MB+)

## Frontend Updates

### Landing Page Component
- ASCII art title
- Two SSO buttons (Google, GitHub)
- Clean, minimal design
- Redirect to upload after auth

### Upload Component
- Large drop zone (full viewport or large section)
- Clear text: "drop at least 1x 10mb image here [PNG/JPG/TIFF/RAW]"
- File size validation feedback
- Format validation feedback
- Upload progress

### Tab Navigation
- Replace current navbar with tab-based navigation
- "My Posts" tab (user's timeline)
- "My Feed" tab (all posts)
- Active state styling

### Post Display
- Show posts in appropriate tab
- Maintain two-column layout for feed
- Single column or full-width for user's own posts (TBD)

## Technical Implementation

### GitHub OAuth Flow
1. Frontend redirects to `/api/auth/github`
2. Backend initiates GitHub OAuth
3. Callback handles token exchange
4. Create/update user with github_id
5. Return JWT token

### File Size Validation
- Frontend: Check file.size before upload
- Backend: Validate Content-Length or file size after read
- Error messages: "Image must be at least 10MB"

### RAW Format Support
- Accept common RAW extensions: .cr2, .nef, .arw, .raf, .orf, .rw2, .pef, .srw
- MIME type handling or extension-based validation
- Store with original extension

## UI/UX Considerations

### Drop Zone
- Large, centered
- Clear visual feedback on drag-over
- File input fallback
- Show selected file name and size
- Validation errors inline

### Tab Switching
- Smooth animation
- Loading states
- Empty states for each tab

### Post Creation
- Immediate feedback
- Optimistic UI updates
- Error handling with retry

---

**Success Criteria**: 
- Landing page with ASCII art and dual SSO (Google + GitHub)
- Post-registration shows large drop zone
- 10MB minimum enforced
- Two-tab navigation (My Posts / My Feed)
- Posts appear in correct tab after upload
- Font stack updated globally
