"""
Context manager for multi-turn clarification flow.

This module manages conversation context and session state to support
clarification questions from the coordinator agent.
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class ConversationContext:
    """Manages conversation context for a single session."""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.query_history: List[str] = []
        self.clarifications: Dict[str, str] = {}
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def add_query(self, query: str) -> None:
        """Add a query to the history."""
        self.query_history.append(query)
        self.last_updated = datetime.now()
    
    def add_clarification(self, question: str, answer: str) -> None:
        """Add a clarification Q&A pair."""
        self.clarifications[question] = answer
        self.last_updated = datetime.now()
    
    def get_full_context(self) -> str:
        """
        Get the full conversation context as a formatted string.
        
        Returns:
            Formatted context string including original query and clarifications
        """
        context_parts = []
        
        if self.query_history:
            context_parts.append(f"Original Query: {self.query_history[0]}")
        
        if self.clarifications:
            context_parts.append("\nClarifications:")
            for question, answer in self.clarifications.items():
                context_parts.append(f"Q: {question}")
                context_parts.append(f"A: {answer}")
        
        return "\n".join(context_parts)
    
    def to_dict(self) -> Dict:
        """Convert context to dictionary format."""
        return {
            "sessionId": self.session_id,
            "queryHistory": self.query_history,
            "clarifications": self.clarifications,
            "createdAt": self.created_at.isoformat(),
            "lastUpdated": self.last_updated.isoformat()
        }


class SessionManager:
    """Manages multiple conversation sessions."""
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.sessions: Dict[str, ConversationContext] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self) -> ConversationContext:
        """Create a new conversation session."""
        context = ConversationContext()
        self.sessions[context.session_id] = context
        return context
    
    def get_session(self, session_id: str) -> Optional[ConversationContext]:
        """
        Get an existing session by ID.
        
        Args:
            session_id: The session identifier
        
        Returns:
            ConversationContext if found and not expired, None otherwise
        """
        context = self.sessions.get(session_id)
        
        if context:
            # Check if session has expired
            if datetime.now() - context.last_updated > self.session_timeout:
                # Session expired, remove it
                del self.sessions[session_id]
                return None
        
        return context
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> ConversationContext:
        """
        Get an existing session or create a new one.
        
        Args:
            session_id: Optional session ID to retrieve
        
        Returns:
            ConversationContext (existing or new)
        """
        if session_id:
            context = self.get_session(session_id)
            if context:
                return context
        
        return self.create_session()
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions from memory.
        
        Returns:
            Number of sessions removed
        """
        now = datetime.now()
        expired_sessions = [
            session_id
            for session_id, context in self.sessions.items()
            if now - context.last_updated > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)
    
    def get_session_count(self) -> int:
        """Get the number of active sessions."""
        return len(self.sessions)


# Global session manager instance
session_manager = SessionManager(session_timeout_minutes=30)
