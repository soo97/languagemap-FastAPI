from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    openai_mock_mode: bool = False
    openai_chat_model: str = "gpt-4.1-mini"

    azure_speech_key: str
    azure_speech_region: str
    azure_speech_endpoint: str | None = None
    azure_speech_voice_name: str = "en-US-JennyNeural"

    youtube_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()