# Meta Prompt V3: All Res Full Res - Polish & Robustness

## Design Updates

### Color Scheme
- **Background**: Very light gentle beige (#FAF9F6 or similar - like evanapplegate.com/cursor agent)
- **Dark Mode**: Full dark mode support with toggle
- **Button Styling**:
  - Hard corners (border-radius: 0)
  - Inactive buttons: 1px stroke border, no fill
  - Active buttons: Light brown fill (#D4C5B9 or similar), no stroke or darker stroke
  - Consistent across all buttons (SSO, tabs, upload, etc.)

### X (Twitter) SSO
- Add X/Twitter OAuth integration
- Third SSO button on landing page
- Backend endpoint: `/api/auth/x` and `/api/auth/x/callback`
- Store `x_id` in User model

## Code Quality & Robustness

### Logging System
- Structured logging with levels (DEBUG, INFO, WARNING, ERROR)
- Log all API requests/responses
- Log authentication events
- Log file uploads (size, type, success/failure)
- Log errors with stack traces
- Use Python `logging` module with proper formatters
- Frontend: Console logging for dev, structured logging for production

### Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Error boundaries in React
- API error handling middleware
- Validation errors clearly displayed
- Network error handling
- File upload error recovery

### DRY Principles
- Extract common button styles to shared CSS
- Reusable form components
- Shared validation functions
- Common API error handling
- Shared utility functions
- Consistent naming conventions

### Bug Prevention
- Input validation (frontend + backend)
- Type checking (TypeScript or PropTypes)
- Null/undefined checks
- Array bounds checking
- File size/type validation
- SQL injection prevention (using ORM)
- XSS prevention (sanitize inputs)
- CSRF protection
- Rate limiting on auth endpoints

### Code Organization
- Consistent file structure
- Clear separation of concerns
- Reusable components
- Utility functions in separate files
- Constants in config files
- Environment-specific configs

### Testing Considerations
- Error scenarios handled
- Edge cases considered
- Input validation tested
- Authentication flows tested

## Implementation Checklist

1. Add X SSO backend integration
2. Update User model with x_id
3. Add X SSO button to landing page
4. Update background color to light beige
5. Implement dark mode toggle (context + localStorage)
6. Update all button styles (hard corners, stroke/fill)
7. Add comprehensive logging system
8. Add error boundaries
9. Extract common styles/components
10. Add input validation utilities
11. Add error handling middleware
12. Update all buttons to use new styling

---

**Success Criteria**: 
- X SSO works end-to-end
- Light beige background throughout
- Dark mode toggle functional
- All buttons have hard corners with proper stroke/fill
- Comprehensive logging in place
- Robust error handling
- DRY codebase with reusable components
- No obvious bugs or edge cases
