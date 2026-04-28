from pydantic import BaseModel, Field

# =========================
# TTS
# =========================

class TtsRequest(BaseModel):
    text: str = Field(...,json_schema_extra={"example": "Hi, welcome! What would you like to order today?"},)

class TtsResponse(BaseModel):
    audioUrl: str

# =========================
# STT
# =========================

class SttResponse(BaseModel):
    recognizedText: str

# =========================
# Pronunciation Assessment
# =========================

class PronunciationAssessmentResponse(BaseModel):
    recognizedText: str
    accuracyScore: float | None = None
    fluencyScore: float | None = None
    completenessScore: float | None = None
    pronunciationScore: float | None = None

# =========================
# Problem Word Audio
# =========================

class ProblemWordAudioRequest(BaseModel):
    word: str = Field(...,json_schema_extra={"example": "almond"},)

class ProblemWordAudioResponse(BaseModel):
    word: str
    audioUrl: str