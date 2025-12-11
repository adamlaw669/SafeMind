from app.core.nlp_model import analyze_risk_level
from typing import Dict, Any

class NLPService:
    """
    Service layer for NLP operations.
    Wraps the core logic to make it easily mockable or replaceable later.
    """
    
    @staticmethod
    async def analyze_report(text: str) -> Dict[str, Any]:
        """
        Analyzes the report text for risk levels.
        """
        if not text:
            return {"risk_level": "low", "score": 0.0}
            
        risk_level = analyze_risk_level(text)
        
        # Simple mapping for MVP
        scores = {
            "high": 0.9,
            "medium": 0.5,
            "low": 0.1
        }
        
        return {
            "risk_level": risk_level,
            "score": scores.get(risk_level, 0.1)
        }

    @staticmethod
    def is_critical(risk_level: str) -> bool:
        """Helper to determine if a risk level requires immediate escalation."""
        return risk_level == "high"