from typing import List
from pydantic import BaseModel, Field

# =========================
# YouTube Search
# =========================

class YoutubeSearchRequest(BaseModel):
    keyword: str = Field(...,json_schema_extra={"example": "cafe English ordering politely"},)
    maxResults: int = Field(
        default=3,
        json_schema_extra={"example": 3},)

class YoutubeVideoItem(BaseModel):
    title: str
    channelTitle: str
    thumbnailUrl: str
    videoUrl: str
    description: str | None = None

class YoutubeSearchResponse(BaseModel):
    youtubePicks: List[YoutubeVideoItem]

# =========================
# Video Summary
# =========================

class VideoSummaryRequest(BaseModel):
    title: str = Field(...,json_schema_extra={"example": "How to Order Coffee in English"},)
    channelTitle: str = Field(...,json_schema_extra={"example": "EnglishClass101"},)
    description: str = Field(
        default="",
        json_schema_extra={"example": "Learn useful English expressions for ordering coffee."},)

class VideoSummaryResponse(BaseModel):
    summary: str