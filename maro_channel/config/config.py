import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")

YOUTUBE_CLIENT_SECRETS_FILE = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "./client_secret.json")

# maro 채널 설정 (마음위로의 약자)
CHANNEL_NAME = "maro (마음위로)"
CHANNEL_SLOGAN = "하루 3분, 당신은 혼자가 아닙니다"
CHANNEL_TITLE_PREFIX = "maro"
CHANNEL_LOCALE = "KR:ko"

# 콘텐츠 타입별 설정
CONTENT_TYPES = {
    "daily_comfort": {
        "duration": "2-3분",
        "upload_frequency": "매일",
        "tags": ["위로", "힐링", "maro", "마음위로", "일상위로"]
    },
    "healing_sound": {
        "duration": "5-10분", 
        "upload_frequency": "주 2회 (화,토)",
        "tags": ["힐링사운드", "자연음", "ASMR", "maro", "마음위로"]
    },
    "overcome_story": {
        "duration": "5-8분",
        "upload_frequency": "주 1회 (수)",
        "tags": ["극복스토리", "동기부여", "희망", "maro", "마음위로"]
    },
    "custom_comfort": {
        "duration": "3-5분",
        "upload_frequency": "주 1회 (금)",
        "tags": ["맞춤위로", "상황별위로", "maro", "마음위로"]
    }
}

VIDEO_RESOLUTION = os.getenv("VIDEO_RESOLUTION", "1920x1080")
BACKGROUND_IMAGE = os.getenv("BACKGROUND_IMAGE", "./background.jpg")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./maro_content")
