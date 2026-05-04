import requests
from app.core.config import settings
from app.ai_coaching.schemas.youtube_schema import (
    YoutubeSearchResponse,
    YoutubeVideoItem,
    VideoSummaryRequest,
)
from app.ai_coaching.services.openai_service import summarize_video_with_llm

def search_youtube_videos(keyword: str,max_results: int,) -> YoutubeSearchResponse:
    if not keyword.strip():
        raise ValueError("Keyword is required.")

    if max_results <= 0:
        raise ValueError("max_results must be greater than 0.")

    if not settings.youtube_api_key:
        return YoutubeSearchResponse(youtubePicks=[])

    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "maxResults": max_results,
        "key": settings.youtube_api_key,}

    response = requests.get(
        url,
        params=params,
        timeout=10,)
    response.raise_for_status()
    data = response.json()
    videos = []

    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        thumbnails = snippet.get("thumbnails", {})
        thumbnail_url = (
                thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url", "")
        )

        description = snippet.get("description", "")

        summary_response = summarize_video_with_llm(
            VideoSummaryRequest(
                title=snippet["title"],
                channelTitle=snippet["channelTitle"],
                description=description,)
        )

        videos.append(
            YoutubeVideoItem(
                title=snippet["title"],
                channelTitle=snippet["channelTitle"],
                thumbnailUrl=thumbnail_url,
                videoUrl=f"https://www.youtube.com/watch?v={video_id}",
                description=description,
                summary=summary_response.summary,)
        )

    return YoutubeSearchResponse(youtubePicks=videos,)