import random
from typing import List, Dict
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_TEXT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

class ComfortContentGenerator:
    """maro 채널용 위로 콘텐츠 생성기 - 세부 기획안 적용"""
    
    def __init__(self):
        self.client = client
