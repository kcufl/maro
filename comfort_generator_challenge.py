import random
from typing import Dict, List
from config import OPENAI_TEXT_MODEL

def generate_one_line_challenge(self, challenge_type: str = None) -> Dict:
    """한 줄 위로 챌린지 (One-Line Comfort Challenge) - 커뮤니티 참여형 (3-5분)"""
    if not challenge_type:
        challenge_types = [
            # 감정 기반 챌린지
            "오늘의 기분", "힘든 순간", "감사한 일", "희망의 메시지",
            "자신을 위한 말", "다른 사람을 위한 위로", "새로운 시작", "꿈과 희망",
            
            # 상황 기반 챌린지
            "아침 인사", "밤 인사", "주말 마무리", "월요일 응원",
            "시험 전날", "면접 전날", "데이트 전날", "여행 전날",
            "생일 축하", "기념일", "계절 변화", "날씨에 따른 위로",
            
            # 테마 기반 챌린지
            "자존감 향상", "자기 사랑", "용기 부여", "희망 전달",
            "감사 표현", "용서", "성장", "변화",
            "인간관계", "가족", "친구", "사랑",
            "일과 삶의 균형", "건강", "꿈과 목표", "성공"
        ]
        challenge_type = random.choice(challenge_types)
    
    # 한 줄 위로 챌린지 전용 구조화된 프롬프트
    prompt = f"""
    {challenge_type}에 대한 "한 줄 위로 챌린지" 콘텐츠를 작성해주세요.
    
    콘텐츠 구조:
    1. 인트로 (15초): "오늘의 한 줄 위로 챌린지: {challenge_type}" + 참여 안내
    2. 챌린지 소개 (30초): 챌린지 목적과 참여 방법 설명
    3. 사용자 댓글 소개 (2-3분): 10-15개의 댓글을 내레이션으로 소개
    4. 챌린지 마무리 (30초): 다음 챌린지 안내와 참여 독려
    5. 아웃트로 (10초): "당신의 한 줄도 누군가에게 위로가 됩니다" + 구독 안내
    
    요구사항:
    1. {challenge_type}와 관련된 다양한 관점의 위로 메시지
    2. 시청자가 참여하고 싶은 흥미로운 챌린지 구성
    3. 실제 사용자 댓글처럼 자연스럽고 공감되는 내용
    4. 3-5분 분량 (약 800-1000자)
    5. 커뮤니티 참여를 유도하는 상호작용적 구성
    6. 다양한 연령대와 상황에 맞는 포용적인 메시지
    7. 자존감 향상과 공동체 의식 함양에 초점
    8. 간단한 애니메이션과 자연 배경으로 구성
    9. 시청자의 참여 욕구를 자극하는 구성
    """
    
    try:
        response = self.client.chat.completions.create(
            model=OPENAI_TEXT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        
        return {
            "type": "one_line_challenge",
            "challenge_type": challenge_type,
            "title": f"한 줄 위로 챌린지: {challenge_type}",
            "content": content,
            "duration": "3-5분",
            "tags": ["한줄위로", "챌린지", "커뮤니티", "maro", "마음위로", "참여", "소통", "위로"],
            "structure": {
                "intro": "15초 - '오늘의 한 줄 위로 챌린지: ~' + 참여 안내",
                "challenge_intro": "30초 - 챌린지 목적과 참여 방법 설명",
                "user_comments": "2-3분 - 10-15개의 댓글을 내레이션으로 소개",
                "challenge_closing": "30초 - 다음 챌린지 안내와 참여 독려",
                "outro": "10초 - '당신의 한 줄도 누군가에게 위로가 됩니다' + 구독 안내"
            },
            "visual_elements": [
                "자연 배경 (하늘, 나무, 꽃 등)",
                "댓글을 보여주는 간단한 애니메이션",
                "참여를 유도하는 시각적 요소"
            ],
            "audio_elements": [
                "밝고 경쾌한 BGM",
                "참여를 독려하는 내레이션",
                "댓글 소개 시 다양한 톤의 내레이션"
            ]
        }
    except Exception as e:
        print(f"한 줄 위로 챌린지 생성 오류: {e}")
        return self._get_fallback_challenge(challenge_type)

def _get_fallback_challenge(self, challenge_type: str) -> Dict:
    """기본 한 줄 위로 챌린지 (API 오류 시)"""
    return {
        "type": "one_line_challenge",
        "challenge_type": challenge_type,
        "title": f"한 줄 위로 챌린지: {challenge_type}",
        "content": f"{challenge_type}에 대한 한 줄 위로를 댓글로 남겨주세요. 당신의 한 줄이 누군가에게 큰 위로가 될 수 있습니다. 함께 위로의 힘을 나누어봐요!",
        "duration": "3-5분",
        "tags": ["한줄위로", "챌린지", "커뮤니티", "maro", "마음위로", "참여", "소통", "위로"],
        "structure": {
            "intro": "15초 - '오늘의 한 줄 위로 챌린지: ~' + 참여 안내",
            "challenge_intro": "30초 - 챌린지 목적과 참여 방법 설명",
            "user_comments": "2-3분 - 10-15개의 댓글을 내레이션으로 소개",
            "challenge_closing": "30초 - 다음 챌린지 안내와 참여 독려",
            "outro": "10초 - '당신의 한 줄도 누군가에게 위로가 됩니다' + 구독 안내"
        }
    }
