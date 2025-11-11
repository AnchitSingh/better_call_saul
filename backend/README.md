# Multi-Agent Advisory System - Backend

Backend server for the Corporate Formation Advisory System powered by Google ADK and Gemini 2.5 Flash.

## Architecture

The backend consists of four main components:

1. **agents.py** - Defines four ADK agents:
   - Tax CPA Agent (tax implications)
   - Legal Attorney Agent (legal compliance)
   - Business Strategist Agent (growth strategy)
   - Coordinator Agent (orchestrates the three specialists)

2. **server.py** - FastAPI server with endpoints:
   - `POST /api/consult` - Main consultation endpoint
   - `GET /api/health` - Health check endpoint

3. **parser.py** - Parses coordinator agent output into structured JSON

4. **context.py** - Manages conversation sessions for clarification flow

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and add your Google API key:

```bash
cp .env.example .env
```

Edit `.env` and configure the following required variables:

#### Required Environment Variables

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `GOOGLE_API_KEY` | Google ADK API key for Gemini 2.5 Flash | `AIza...` (obtain from Google AI Studio) |
| `HOST` | Server host address | `0.0.0.0` (default) |
| `PORT` | Server port number | `8000` (default) |
| `ENVIRONMENT` | Environment mode (development or production) | `development` (default) |
| `FRONTEND_ORIGIN` | Frontend origin for CORS | `http://localhost:5173` (development) |

**Getting a Google API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key or use an existing one
3. Copy the key and paste it into your `.env` file

**Example `.env` file:**
```
GOOGLE_API_KEY=AIzaSyC_your_actual_api_key_here
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
FRONTEND_ORIGIN=http://localhost:5173
```

### 4. Run the Server

```bash
python server.py
```

Or with uvicorn directly:
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /api/consult

Submit a business formation query.

**Request:**
```json
{
  "query": "I'm starting a tech startup with 2 co-founders...",
  "context": {
    "sessionId": "optional-session-id",
    "clarificationAnswer": "optional-answer-to-previous-question"
  }
}
```

**Response:**
```json
{
  "recommendedStructure": "C-Corp",
  "keyBenefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
  "tradeOffs": ["Trade-off 1", "Trade-off 2"],
  "nextSteps": ["Step 1", "Step 2", "Step 3"],
  "conflicts": [
    {
      "area": "Tax vs Fundraising",
      "description": "...",
      "resolution": "..."
    }
  ],
  "needsClarification": false,
  "clarificationQuestion": null,
  "sessionId": "session-uuid"
}
```

### GET /api/health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "agents": ["TaxCPA", "CorporateAttorney", "BusinessStrategist", "Coordinator"],
  "active_sessions": 5
}
```

## Agent System

The coordinator agent orchestrates three specialist agents in parallel:

1. **Tax CPA Agent** analyzes tax implications (pass-through vs double taxation, QBI deductions, etc.)
2. **Legal Attorney Agent** assesses legal compliance and liability protection
3. **Business Strategist Agent** evaluates growth trajectory and scalability

The coordinator synthesizes their recommendations, identifies conflicts, and provides a unified response.

## Security Features

### Rate Limiting

The API implements rate limiting to prevent abuse:
- **Consultation endpoint** (`/api/consult`): 10 requests per minute per IP address
- **Health check endpoint** (`/api/health`): 30 requests per minute per IP address

When rate limit is exceeded, the API returns HTTP 429 (Too Many Requests).

### Security Headers

The following security headers are automatically added to all responses:

- **Strict-Transport-Security (HSTS)**: Enforces HTTPS in production
- **Content-Security-Policy (CSP)**: Restricts resource loading to prevent XSS attacks
- **X-Frame-Options**: Prevents clickjacking by denying iframe embedding
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-XSS-Protection**: Enables browser XSS filtering
- **Referrer-Policy**: Controls referrer information
- **Permissions-Policy**: Restricts browser features (geolocation, camera, microphone)

### CORS Configuration

- **Development**: Allows all origins for easier testing
- **Production**: Only allows the specific frontend origin set in `FRONTEND_ORIGIN`

Set `ENVIRONMENT=production` to enable production security settings.

## Error Handling

- Input validation (query length 10-5000 characters)
- Agent execution error handling with appropriate HTTP status codes
- Graceful parsing fallbacks
- Comprehensive logging for debugging
- Rate limit enforcement with clear error messages

## Session Management

Sessions are maintained for 30 minutes to support multi-turn clarification flows. Expired sessions are automatically cleaned up.

## Development

### Testing Modules

Test individual modules:

```bash
# Test parser
python3 -c "import sys; sys.path.insert(0, '.'); from parser import parse_agent_response; print('Parser OK')"

# Test context manager
python3 -c "import sys; sys.path.insert(0, '.'); from context import ConversationContext; print('Context OK')"
```

### Logging

Logs are written to stdout with INFO level by default. Adjust in `server.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # For more verbose logging
```

## Docker Deployment

### Using Docker Compose (Recommended)

The easiest way to run the backend in a containerized environment:

```bash
# Ensure .env file is configured
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop the container
docker-compose down
```

### Using Docker Directly

Build and run the Docker container manually:

```bash
# Build the image
docker build -t advisory-backend .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  -e FRONTEND_ORIGIN=http://localhost:5173 \
  --name advisory-backend \
  advisory-backend

# View logs
docker logs -f advisory-backend

# Stop the container
docker stop advisory-backend
docker rm advisory-backend
```

### Docker Configuration Files

- **Dockerfile**: Multi-stage build for optimized image size
- **docker-compose.yml**: Orchestration configuration for local development
- **.dockerignore**: Excludes unnecessary files from the image

### Production Deployment

For production deployments, set appropriate environment variables:

```bash
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_production_key \
  -e FRONTEND_ORIGIN=https://your-frontend-domain.com \
  -e PORT=8000 \
  --restart unless-stopped \
  --name advisory-backend \
  advisory-backend
```

The container includes a health check that monitors the `/api/health` endpoint.

## Requirements

- Python 3.10+
- FastAPI 0.115.5
- google-genai 0.3.0 (includes ADK)
- uvicorn 0.32.1
- pydantic 2.10.3
- python-dotenv 1.0.1

## Deployment Platforms

The backend can be deployed to various platforms:

- **Google Cloud Run**: Deploy the Docker container directly
- **AWS ECS/Fargate**: Use the Dockerfile for container deployment
- **Heroku**: Use the Dockerfile or Python buildpack
- **DigitalOcean App Platform**: Deploy from GitHub with Dockerfile
- **Railway**: Connect GitHub repo and deploy automatically
