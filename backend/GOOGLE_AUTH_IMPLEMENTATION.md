# Google Authentication Implementation

## Overview
The SafeMind backend now supports Google OAuth sign-in integrated with FastAPI. The implementation handles OAuth login redirects, callback processing, user creation or updates in PostgreSQL (via SQLAlchemy), and application-level JWT generation for authenticated sessions.

## Environment Variables
Configure the following keys in a `.env` file (refer to `.env.example` for structure):

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI` (defaults to `http://localhost:8000/api/auth/google/callback`)
- `JWT_SECRET`
- `JWT_ALGORITHM` (defaults to `HS256`)
- `DATABASE_URL` (PostgreSQL connection string)

## Application Changes
- `app/core/config.py`: centralised environment loading with Pydantic settings.
- `app/core/security.py`: JWT token factory with a 24-hour default expiry.
- `app/db/base.py` and `app/db/__init__.py`: SQLAlchemy engine, session factory, and dependency wiring.
- `app/models/user.py`: user model with Google metadata and verification flag.
- `app/schemas/user_schema.py`: request and response schemas using Pydantic v2.
- `app/routers/auth_router.py`: routes for Google login, callback, and frontend token verification.
- `app/main.py`: FastAPI setup that registers the auth router and prepares database tables.
- `app/test/test_auth.py`: test suite covering redirects, callback processing, and token verification.

## Auth Workflow
1. `GET /api/auth/google/login` redirect users to Google’s OAuth consent screen.
2. `GET /api/auth/google/callback` exchanges the authorization code, verifies the ID token, persists the user, and returns an application JWT.
3. `POST /api/auth/google/verify` validates a frontend-provided credential token, ensures the user exists, and issues a JWT.

## Testing
Run the tests after installing requirements:
```bash
pip install -r requirement.txt
pytest
```
Tests mock Google’s endpoints to validate token exchange, user persistence, and JWT issuance without external calls.

## Next Steps
- Configure production Google OAuth credentials and JWT secrets.
- Consider adding session management (e.g., Redis) or multi-factor workflows as the platform evolves.
