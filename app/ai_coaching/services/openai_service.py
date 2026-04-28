import json
from openai import OpenAI
from app.core.config import settings
from app.ai_coaching.prompts.coaching_script_prompt_builder import build_coaching_script_prompt
from app.ai_coaching.prompts.final_feedback_prompt_builder import build_final_feedback_prompt
from app.ai_coaching.prompts.recommend_sentences_prompt_builder import (build_recommend_sentences_prompt,)
from app.ai_coaching.prompts.youtube_keywords_prompt_builder import (build_youtube_keywords_prompt,)
from app.ai_coaching.prompts.video_summary_prompt_builder import build_video_summary_prompt
from app.ai_coaching.schemas.youtube_schema import (VideoSummaryRequest,VideoSummaryResponse,)
from app.ai_coaching.schemas.openai_schema import (
    CoachingScriptItem,
    CoachingScriptRequest,
    CoachingScriptResponse,
    FeedbackSection,
    FinalFeedbackRequest,
    FinalFeedbackResponse,
    ProblemWord,
    PronunciationSection,
    RecommendSentencesRequest,
    RecommendSentencesResponse,
    YoutubeKeywordsRequest,
    YoutubeKeywordsResponse,)

# =========================
# OpenAI Client
# =========================
client = OpenAI(api_key=settings.openai_api_key)

# =========================
# Internal JSON Helpers
# =========================
def _extract_text(response) -> str:
    return response.output_text

def _safe_json_loads(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1

        if 0 <= start < end:
            return json.loads(text[start:end])

        raise

def _request_json(prompt: str) -> dict:
    if not prompt.strip():
        raise ValueError("Prompt is required.")

    response = client.responses.create(
        model=settings.openai_chat_model,
        input=prompt,)

    return _safe_json_loads(_extract_text(response))

# =========================
# Coaching Script
# =========================
def generate_coaching_script(request: CoachingScriptRequest) -> CoachingScriptResponse:
    if settings.openai_mock_mode:
        return CoachingScriptResponse(
            messages=[
                CoachingScriptItem(
                    role="ASSISTANT",
                    message="Hi, welcome! What would you like to order today?",),
                CoachingScriptItem(
                    role="USER",
                    message="I would like a latte with almond milk, please.",),
                CoachingScriptItem(
                    role="ASSISTANT",
                    message="Sure. Would you like it hot or iced?",),
                CoachingScriptItem(
                    role="USER",
                    message="I would like it iced, please.",),
            ]
        )

    prompt = build_coaching_script_prompt(
        option_type=request.optionType,
        place_name=request.placeName,
        country=request.country,
        city=request.city,
        place_address=request.placeAddress,
        scenario_prompt=request.scenarioPrompt,
        evaluation=request.evaluation,
        previous_messages=request.previousMessages,)

    data = _request_json(prompt)

    return CoachingScriptResponse(
        messages=[
            CoachingScriptItem(
                role=item["role"],
                message=item["message"],)
            for item in data["messages"]
        ]
    )


# =========================
# Final Feedback
# =========================
def generate_final_feedback(request: FinalFeedbackRequest) -> FinalFeedbackResponse:
    if not request.messages:
        raise ValueError("Conversation messages are required.")

    if settings.openai_mock_mode:
        return FinalFeedbackResponse(
            totalScore=87,
            summaryFeedback="전체적으로 자연스럽게 응답했지만 일부 발음은 더 확인하면 좋습니다.",
            naturalness=FeedbackSection(
                level="GOOD",
                comment="문장이 자연스럽게 이어졌어요.",),
            flow=FeedbackSection(
                level="GOOD",
                comment="질문에 맞게 빠르게 이어졌어요.",),
            pronunciation=PronunciationSection(
                level="CHECK",
                comment="preferably, almond 발음을 다시 확인해보세요.",
                problemWords=[
                    ProblemWord(word="preferably"),
                    ProblemWord(word="almond"),
                ],
            ),
        )

    prompt = build_final_feedback_prompt(
        messages=request.messages,
        pronunciation_results=request.pronunciationResults,)

    data = _request_json(prompt)

    return FinalFeedbackResponse(**data)

# =========================
# Recommend Sentences
# =========================
def generate_recommend_sentences(request: RecommendSentencesRequest,) -> RecommendSentencesResponse:
    if not request.finalFeedback.strip():
        raise ValueError("Final feedback is required.")

    if settings.openai_mock_mode:
        return RecommendSentencesResponse(
            sentences=[
                "Could I get a latte with almond milk, please?",
                "Would it be possible to make it less sweet?",
                "Could you recommend something popular here?",]
        )

    prompt = build_recommend_sentences_prompt(final_feedback=request.finalFeedback,)
    data = _request_json(prompt)
    return RecommendSentencesResponse(**data)

# =========================
# YouTube Keywords
# =========================
def generate_youtube_keywords(request: YoutubeKeywordsRequest,) -> YoutubeKeywordsResponse:
    if not request.finalFeedback.strip():
        raise ValueError("Final feedback is required.")

    if settings.openai_mock_mode:
        return YoutubeKeywordsResponse(
            keywords=[
                "cafe English ordering politely",
                "English pronunciation almond",
                "travel English cafe dialogue",]
        )

    prompt = build_youtube_keywords_prompt(
        final_feedback=request.finalFeedback,)
    data = _request_json(prompt)
    return YoutubeKeywordsResponse(**data)

# =========================
# Video Summary
# =========================
def summarize_video_with_llm(request: VideoSummaryRequest) -> VideoSummaryResponse:
    if not request.title.strip():
        raise ValueError("Video title is required.")

    if settings.openai_mock_mode:
        return VideoSummaryResponse(
            summary="카페에서 정중하게 주문하는 표현을 연습하기 좋은 영상입니다.")

    prompt = build_video_summary_prompt(
        title=request.title,
        channel_title=request.channelTitle,
        description=request.description,)

    data = _request_json(prompt)
    return VideoSummaryResponse(**data)