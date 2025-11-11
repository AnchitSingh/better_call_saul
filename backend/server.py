"""
FastAPI server for the Multi-Agent Corporate Formation Advisory System.

This server exposes HTTP endpoints for the frontend to interact with
the ADK agent system.
"""

import os
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from agents import root_agent
from parser import parse_agent_response
from context import session_manager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Advisory System",
    description="Corporate formation advisory system powered by Google ADK",
    version="1.0.0"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
# In production, only allow specific frontend origin
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# In production, only allow the specific frontend origin
allowed_origins = [FRONTEND_ORIGIN]
if ENVIRONMENT == "development":
    allowed_origins.append("*")  # Allow all for development

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Strict-Transport-Security (HSTS)
    if ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Content-Security-Policy (CSP)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' https://generativelanguage.googleapis.com; "
        "frame-ancestors 'none';"
    )
    
    # X-Frame-Options
    response.headers["X-Frame-Options"] = "DENY"
    
    # X-Content-Type-Options
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-XSS-Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Referrer-Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions-Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

# Add rate limiting middleware
app.add_middleware(SlowAPIMiddleware)


# Request/Response Models
class ConsultRequest(BaseModel):
    """Request model for consultation endpoint."""
    query: str = Field(..., min_length=10, max_length=5000)
    context: Optional[Dict[str, Any]] = None
    
    @validator('query')
    def validate_query(cls, v):
        """Validate query is not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError('Query cannot be empty')
        return v.strip()


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    agents: list[str]
    active_sessions: int


@app.get("/api/health", response_model=HealthResponse)
@limiter.limit("30/minute")  # Allow more frequent health checks
async def health_check(request: Request):
    """
    Health check endpoint to verify service is running.
    
    Returns:
        HealthResponse with service status and agent list
    """
    try:
        # Cleanup expired sessions
        session_manager.cleanup_expired_sessions()
        
        return HealthResponse(
            status="healthy",
            agents=["TaxCPA", "CorporateAttorney", "BusinessStrategist", "Coordinator"],
            active_sessions=session_manager.get_session_count()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unhealthy")


@app.post("/api/consult")
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute per IP
async def consult(request: ConsultRequest, http_request: Request):
    """
    Main consultation endpoint that processes user queries through the agent system.
    
    Rate limited to 10 requests per minute per IP address.
    
    Args:
        request: ConsultRequest with query and optional context
        http_request: FastAPI Request object for logging
    
    Returns:
        Structured recommendation response
    
    Raises:
        HTTPException: For various error conditions
    """
    client_ip = http_request.client.host if http_request.client else "unknown"
    logger.info(f"Consultation request from {client_ip}: {request.query[:100]}...")
    
    try:
        # Get or create session
        session_id = None
        if request.context and "sessionId" in request.context:
            session_id = request.context["sessionId"]
        
        conversation_context = session_manager.get_or_create_session(session_id)
        
        # Add query to history
        conversation_context.add_query(request.query)
        
        # Build full context for agent
        full_query = request.query
        if conversation_context.clarifications:
            context_str = conversation_context.get_full_context()
            full_query = f"{context_str}\n\nCurrent Query: {request.query}"
        
        logger.info(f"Executing agent with session {conversation_context.session_id}")
        
        # Execute the root agent
        try:
            response = root_agent.generate_content(full_query)
            agent_output = response.text
            
            logger.info(f"Agent execution completed. Response length: {len(agent_output)}")
            logger.debug(f"Agent response: {agent_output[:500]}...")
            
        except Exception as agent_error:
            logger.error(f"Agent execution error: {agent_error}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Agent execution failed. Please try again."
            )
        
        # Parse the agent response
        try:
            parsed_response = parse_agent_response(agent_output)
            response_dict = parsed_response.to_dict()
            
            # Add session ID to response
            response_dict["sessionId"] = conversation_context.session_id
            
            # If this was a clarification, store it
            if parsed_response.needs_clarification and request.context:
                if "clarificationAnswer" in request.context:
                    conversation_context.add_clarification(
                        parsed_response.clarification_question,
                        request.context["clarificationAnswer"]
                    )
            
            logger.info(f"Response parsed successfully. Needs clarification: {parsed_response.needs_clarification}")
            
            return response_dict
            
        except Exception as parse_error:
            logger.error(f"Response parsing error: {parse_error}", exc_info=True)
            # Return raw response if parsing fails
            return {
                "recommendedStructure": "Unable to parse response",
                "keyBenefits": ["Please review the raw response"],
                "tradeOffs": ["Parsing error occurred"],
                "nextSteps": ["Contact support"],
                "conflicts": [],
                "rawResponse": agent_output,
                "sessionId": conversation_context.session_id
            }
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error in consultation endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return HTTPException(
        status_code=500,
        detail="Internal server error"
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
