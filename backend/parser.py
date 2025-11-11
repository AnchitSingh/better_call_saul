"""
Response parser for coordinator agent output.

This module parses the structured text output from the coordinator agent
and converts it into structured JSON format for the API response.
"""

import re
from typing import List, Optional, Dict, Any


class ConflictDetail:
    """Represents a conflict between specialist recommendations."""
    
    def __init__(self, area: str, description: str, resolution: str):
        self.area = area
        self.description = description
        self.resolution = resolution
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "area": self.area,
            "description": self.description,
            "resolution": self.resolution
        }


class RecommendationResponse:
    """Structured recommendation response."""
    
    def __init__(
        self,
        recommended_structure: str,
        key_benefits: List[str],
        trade_offs: List[str],
        next_steps: List[str],
        conflicts: Optional[List[ConflictDetail]] = None,
        needs_clarification: bool = False,
        clarification_question: Optional[str] = None
    ):
        self.recommended_structure = recommended_structure
        self.key_benefits = key_benefits
        self.trade_offs = trade_offs
        self.next_steps = next_steps
        self.conflicts = conflicts or []
        self.needs_clarification = needs_clarification
        self.clarification_question = clarification_question
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommendedStructure": self.recommended_structure,
            "keyBenefits": self.key_benefits,
            "tradeOffs": self.trade_offs,
            "nextSteps": self.next_steps,
            "conflicts": [c.to_dict() for c in self.conflicts],
            "needsClarification": self.needs_clarification,
            "clarificationQuestion": self.clarification_question
        }


def extract_section(text: str, section_name: str) -> List[str]:
    """
    Extract bullet points or numbered items from a section.
    
    Args:
        text: The full text to search
        section_name: The section header to find (e.g., "KEY BENEFITS")
    
    Returns:
        List of items found in that section
    """
    # Find the section header
    section_pattern = rf"##\s*{re.escape(section_name)}\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(section_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    section_content = match.group(1).strip()
    
    # Extract bullet points (- item) or numbered items (1. item)
    items = []
    for line in section_content.split('\n'):
        line = line.strip()
        # Match bullet points or numbered lists
        if re.match(r'^[-*]\s+', line):
            items.append(re.sub(r'^[-*]\s+', '', line).strip())
        elif re.match(r'^\d+\.\s+', line):
            items.append(re.sub(r'^\d+\.\s+', '', line).strip())
    
    return items


def identify_conflicts(text: str) -> List[ConflictDetail]:
    """
    Extract conflict information from the CONFLICTS IDENTIFIED section.
    
    Args:
        text: The full coordinator response text
    
    Returns:
        List of ConflictDetail objects
    """
    # Find the conflicts section
    conflicts_pattern = r"##\s*CONFLICTS IDENTIFIED\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(conflicts_pattern, text, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return []
    
    conflicts_content = match.group(1).strip()
    
    # Check if no conflicts
    if "no significant conflicts" in conflicts_content.lower():
        return []
    
    conflicts = []
    
    # Parse conflict blocks with Area, Description, Resolution
    # Pattern: - **Area**: [text]\n  - **Description**: [text]\n  - **Resolution**: [text]
    conflict_blocks = re.findall(
        r'-\s*\*\*Area\*\*:\s*(.+?)\n\s*-\s*\*\*Description\*\*:\s*(.+?)\n\s*-\s*\*\*Resolution\*\*:\s*(.+?)(?=\n-\s*\*\*Area\*\*:|\Z)',
        conflicts_content,
        re.DOTALL | re.IGNORECASE
    )
    
    for area, description, resolution in conflict_blocks:
        conflicts.append(ConflictDetail(
            area=area.strip(),
            description=description.strip(),
            resolution=resolution.strip()
        ))
    
    return conflicts


def parse_agent_response(text: str) -> RecommendationResponse:
    """
    Parse the coordinator agent's text response into structured format.
    
    Args:
        text: The raw text output from the coordinator agent
    
    Returns:
        RecommendationResponse object with structured data
    
    Raises:
        ValueError: If the response cannot be parsed
    """
    try:
        # Check if this is a clarification request
        if "clarification" in text.lower() and "?" in text:
            # Extract the question
            lines = text.strip().split('\n')
            question = None
            for line in lines:
                if '?' in line:
                    question = line.strip()
                    break
            
            if question:
                return RecommendationResponse(
                    recommended_structure="",
                    key_benefits=[],
                    trade_offs=[],
                    next_steps=[],
                    needs_clarification=True,
                    clarification_question=question
                )
        
        # Extract recommended structure
        structure_pattern = r"##\s*RECOMMENDED STRUCTURE\s*\n(.*?)(?=\n##|\Z)"
        structure_match = re.search(structure_pattern, text, re.DOTALL | re.IGNORECASE)
        recommended_structure = structure_match.group(1).strip() if structure_match else "Unable to determine"
        
        # Extract sections
        key_benefits = extract_section(text, "KEY BENEFITS")
        trade_offs = extract_section(text, "TRADE-OFFS")
        next_steps = extract_section(text, "NEXT STEPS")
        conflicts = identify_conflicts(text)
        
        # Fallback values if sections are empty
        if not key_benefits:
            key_benefits = ["Analysis in progress - please review full response"]
        if not trade_offs:
            trade_offs = ["Analysis in progress - please review full response"]
        if not next_steps:
            next_steps = ["Consult with professional advisors", "Review full analysis", "Make informed decision"]
        
        return RecommendationResponse(
            recommended_structure=recommended_structure,
            key_benefits=key_benefits,
            trade_offs=trade_offs,
            next_steps=next_steps,
            conflicts=conflicts
        )
    
    except Exception as e:
        # Graceful fallback for parsing errors
        return RecommendationResponse(
            recommended_structure="Unable to parse recommendation",
            key_benefits=["Please review the full response for details"],
            trade_offs=["Parsing error occurred"],
            next_steps=["Contact support if this issue persists"],
            conflicts=[]
        )
