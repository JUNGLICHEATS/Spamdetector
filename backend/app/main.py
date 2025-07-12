from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
import uvicorn
from datetime import datetime

# Import our modules
from app.ml.classifier import SpamClassifier
from app.ml.rules import RulesEngine

# Initialize FastAPI app
app = FastAPI(
    title="SpamGuard API",
    description="AI-Powered Spam Detection System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
spam_classifier = SpamClassifier()
rule_engine = RulesEngine()

# Pydantic models
class MessageRequest(BaseModel):
    message: str
    options: Optional[Dict[str, Any]] = {}

class ClassificationResponse(BaseModel):
    classification: str
    confidence: float
    processing_time: int
    details: Optional[Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {"message": "SpamGuard API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/classify", response_model=ClassificationResponse)
async def classify_message(request: MessageRequest):
    """Main endpoint for message classification"""
    try:
        start_time = datetime.now()
        
        # Rule-based classification
        rule_result = rule_engine.analyze_message(request.message)
        
        # ML classification
        ml_result = spam_classifier.predict(request.message)
        
        # Combine results
        final_confidence = (rule_result['confidence'] + ml_result['confidence']) / 2
        
        if final_confidence > 0.7:
            classification = "spam"
        elif final_confidence < 0.3:
            classification = "ham"
        else:
            classification = "uncertain"
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Extract triggered rules for the response
        triggered_rules = [detail["rule_name"] for detail in rule_result.get('rule_details', [])]
        
        # Prepare response
        response = ClassificationResponse(
            classification=classification,
            confidence=round(final_confidence, 3),
            processing_time=processing_time,
            details={
                "rule_details": rule_result.get('rule_details', []),
                "ml_confidence": ml_result['confidence'],
                "triggered_rules": triggered_rules
            } if request.options.get("include_details", False) else {}
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")

if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)