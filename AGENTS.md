# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Project Details

### Dual Protocol Architecture
- **Single server** exposes both REST API and MCP protocol on port 8080
- **MCP must be created BEFORE FastAPI** - lifespan combination requires this order (see server.py:14-16)
- REST endpoints at `/api/*`, MCP tools at `/mcp`
- Same business logic in `services/` layer used by both protocols

### Backend (Python/FastAPI)
- **Service layer pattern**: Business logic in `services/`, NOT in route handlers
- **Error responses**: Services return `ErrorResponse | SuccessType | Duplicate` union types (not exceptions)
- **Database sessions**: Each MCP tool creates/closes its own session (no dependency injection)
- **Booking validation**: Requires BOTH `user_id` AND `name` match (see services/booking.py:27)
- **Frequent traveller auto-upgrade**: `check_and_upgrade_status()` called AFTER incrementing `total_bookings` (services/booking.py:60-62)
- **Status upgrade thresholds**: Bronze(5), Silver(10), Gold(20), Platinum(50) - hardcoded in services/user.py:73-84
- **Test command**: `pytest` from backend directory (uses pytest.ini config)

### Frontend (React/TypeScript)
- **API base URL**: Uses `VITE_API_URL` env var, defaults to `http://localhost:8080`
- **User persistence**: Stored in localStorage with key `galaxium_user` (see hooks/useUser.tsx:7)
- **Error handling**: Backend errors have `success: false` field to distinguish from success responses
- **API client**: Axios interceptor transforms all errors to `ErrorResponse` format (see services/api.ts:20-35)

### Startup
- **start.sh**: Automatically creates venv, installs deps, starts both servers
- **Backend port**: 8080 (hardcoded in server.py)
- **Frontend port**: 5173 (Vite default)
- **Database**: SQLite file created on first run, seeded with demo data

### Development Workflow
- Backend changes: Restart `python server.py`
- Frontend changes: Vite hot-reloads automatically
- Tests: Run `pytest` from `booking_system_backend/` directory
- Build frontend: `npm run build` creates `dist/` folder