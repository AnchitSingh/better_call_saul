# Multi-Agent Corporate Formation Advisory System

A full-stack application that coordinates three specialist AI agents (Tax CPA, Legal Attorney, Business Strategist) to provide unified business formation advice. Built with React, Python, Google ADK, and Gemini 2.5 Flash.

## Architecture

```
┌─────────┐      HTTPS      ┌──────────────┐      API       ┌─────────────┐
│  User   │ ◄──────────────► │ React + Vite │ ◄────────────► │ ADK Server  │
│ Browser │                  │   Frontend   │                │  (Python)   │
└─────────┘                  └──────────────┘                └──────┬──────┘
                                                                     │
                                                                     ▼
                                                            ┌────────────────┐
                                                            │  Coordinator   │
                                                            │     Agent      │
                                                            └────────┬───────┘
                                                                     │
                                    ┌────────────────────────────────┼────────────────────────┐
                                    │                                │                        │
                                    ▼                                ▼                        ▼
                            ┌───────────────┐              ┌─────────────────┐      ┌──────────────────┐
                            │   Tax CPA     │              │ Legal Attorney  │      │    Business      │
                            │     Agent     │              │      Agent      │      │  Strategist      │
                            └───────────────┘              └─────────────────┘      │      Agent       │
                                                                                     └──────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google API Key (get from [Google AI Studio](https://aistudio.google.com/apikey))

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd multi-agent-advisory-system
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

**Required Backend Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google ADK API key | `AIza...` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `FRONTEND_URL` | Frontend origin for CORS | `http://localhost:5173` |

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env if needed (default: http://localhost:8000)
```

**Required Frontend Environment Variables:**

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python server.py
```

Backend will be available at `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 5. Test the System

1. Open `http://localhost:5173` in your browser
2. Enter a business formation query, for example:

**Example Query 1 - Tech Startup:**
```
I'm starting a tech startup with 2 co-founders. We plan to raise VC funding 
within 12 months. What business structure should we choose?
```

**Example Query 2 - Consulting Business:**
```
I'm a solo consultant making $150K/year. I want to minimize taxes and keep 
things simple. Should I form an LLC or S-Corp?
```

**Example Query 3 - E-commerce Business:**
```
I'm launching an e-commerce business selling physical products. I'll be the 
sole owner initially but may bring on partners later. What entity type makes sense?
```

**Example Query 4 - Real Estate Investment:**
```
I'm buying rental properties with a business partner. We want liability 
protection and tax efficiency. What structure should we use?
```

3. Wait for the coordinated recommendation from all three specialist agents (~5 seconds)
4. Review the recommended structure, benefits, trade-offs, and next steps
5. If the system requests clarification, provide additional context and resubmit

## Project Structure

```
.
├── backend/                 # Python backend with ADK agents
│   ├── agents.py           # Agent definitions
│   ├── server.py           # FastAPI server
│   ├── parser.py           # Response parser
│   ├── context.py          # Session management
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── types/         # TypeScript interfaces
│   │   └── App.tsx        # Main app component
│   ├── package.json       # Node dependencies
│   └── .env.example       # Environment template
└── README.md              # This file
```

## API Documentation

### POST /api/consult

Submit a business formation query.

**Request:**
```json
{
  "query": "I'm starting a tech startup...",
  "context": {
    "sessionId": "optional-session-id"
  }
}
```

**Response:**
```json
{
  "recommendedStructure": "C-Corp",
  "keyBenefits": ["Benefit 1", "Benefit 2"],
  "tradeOffs": ["Trade-off 1", "Trade-off 2"],
  "nextSteps": ["Step 1", "Step 2"],
  "conflicts": [
    {
      "area": "Tax vs Fundraising",
      "description": "...",
      "resolution": "..."
    }
  ]
}
```

### GET /api/health

Check service health.

**Response:**
```json
{
  "status": "healthy",
  "agents": ["TaxCPA", "CorporateAttorney", "BusinessStrategist", "Coordinator"]
}
```

## How It Works

1. **User submits query** through the React frontend
2. **Coordinator agent** receives the query and delegates to three specialist agents in parallel:
   - **Tax CPA Agent**: Analyzes tax implications (pass-through vs double taxation, QBI deductions, etc.)
   - **Legal Attorney Agent**: Assesses legal compliance and liability protection
   - **Business Strategist Agent**: Evaluates growth trajectory and scalability
3. **Coordinator synthesizes** recommendations, identifies conflicts, and provides unified advice
4. **Frontend displays** structured recommendation with benefits, trade-offs, and next steps

## Features

- ✅ Parallel agent execution for fast responses (~5 seconds)
- ✅ Conflict identification between different professional perspectives
- ✅ Structured recommendations with clear next steps
- ✅ Multi-turn clarification flow for incomplete queries
- ✅ Error handling and graceful degradation
- ✅ Session management for conversation context

## Technology Stack

**Frontend:**
- React 18 + TypeScript
- Vite for build tooling
- CSS for styling

**Backend:**
- Python 3.10+
- Google Agent Development Kit (ADK)
- Gemini 2.5 Flash
- FastAPI
- Uvicorn

## Deployment

### Docker Deployment (Recommended)

The backend includes Docker configuration for easy deployment.

**1. Build and run with Docker Compose:**

```bash
cd backend

# Create .env file with your configuration
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

**2. Build Docker image manually:**

```bash
cd backend

# Build the image
docker build -t advisory-backend .

# Run the container
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_API_KEY=your_api_key \
  -e FRONTEND_ORIGIN=https://your-frontend-domain.com \
  --name advisory-backend \
  advisory-backend
```

### Production Deployment

**Backend (Python):**

Deploy to any platform that supports Docker or Python applications:

- **Google Cloud Run**: Deploy the Docker container directly
- **AWS ECS/Fargate**: Use the Dockerfile for container deployment
- **Heroku**: Use the Dockerfile or Python buildpack
- **DigitalOcean App Platform**: Deploy from GitHub with Dockerfile

**Environment Variables for Production:**
```bash
GOOGLE_API_KEY=your_production_api_key
PORT=8000
FRONTEND_ORIGIN=https://your-frontend-domain.com
```

**Frontend (React):**

Build and deploy the static site:

```bash
cd frontend

# Build for production
npm run build

# The dist/ folder contains the production build
# Deploy to any static hosting service
```

Deploy to:
- **Vercel**: Connect GitHub repo, auto-deploys on push
- **Netlify**: Drag-and-drop `dist/` folder or connect GitHub
- **AWS S3 + CloudFront**: Upload `dist/` to S3 bucket
- **GitHub Pages**: Use GitHub Actions to deploy `dist/`

**Frontend Environment Variables for Production:**
```bash
VITE_API_URL=https://your-backend-domain.com
```

### Example Deployment Workflow

1. **Deploy Backend:**
   ```bash
   # Build and push Docker image
   docker build -t your-registry/advisory-backend:latest backend/
   docker push your-registry/advisory-backend:latest
   
   # Deploy to your platform (example: Cloud Run)
   gcloud run deploy advisory-backend \
     --image your-registry/advisory-backend:latest \
     --platform managed \
     --region us-central1 \
     --set-env-vars GOOGLE_API_KEY=your_key
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   
   # Set production API URL
   echo "VITE_API_URL=https://your-backend-url.com" > .env.production
   
   # Build
   npm run build
   
   # Deploy to Vercel
   vercel --prod
   ```

### Health Monitoring

The backend includes a health check endpoint at `/api/health`. Configure your deployment platform to use this for:
- Container health checks
- Load balancer health probes
- Uptime monitoring

## Development

See individual README files for detailed development instructions:
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## Troubleshooting

### Backend won't start
- Verify `GOOGLE_API_KEY` is set in `backend/.env`
- Check Python version: `python3 --version` (should be 3.10+)
- Ensure virtual environment is activated

### Frontend can't connect to backend
- Verify backend is running on `http://localhost:8000`
- Check `VITE_API_URL` in `frontend/.env`
- Check browser console for CORS errors

### Agents not responding
- Verify Google API key is valid
- Check backend logs for error messages
- Ensure you have internet connectivity

## License

[Add your license here]
