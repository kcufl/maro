import random
from typing import Dict
from config import OPENAI_TEXT_MODEL

def generate_healing_sound_script(self, sound_type: str = None) -> Dict:
    """힐링 사운드 + 멘트 (ASMR Comfort) - 장시간 시청용 (5-10분)"""
    if not sound_type:
        sound_types = ["빗소리", "바람소리", "숲속소리", "파도소리", "새소리", "계곡물소리", "불꽃소리", "바다파도소리"]
        sound_type = random.choice(sound_types)
    
    # 힐링 사운드 전용 구조화된 프롬프트
    prompt = f"""
    {sound_type}와 함께 들을 수 있는 "힐링 사운드 + 멘트" 콘텐츠를 작성해주세요.
    
    콘텐츠 구조:
    1. 인트로 (10초): "오늘은 {sound_type}와 함께, 위로의 시간을 준비했습니다."
    2. 자연 사운드 (5-10분): {sound_type} 루프 편집으로 끊김 없이 연결
    3. 위로 멘트 (1-2분 간격으로 삽입): 짧은 멘트 3-4개
    4. 아웃트로: "오늘도 수고 많았습니다. 편안한 밤 되세요."
    
    요구사항:
    1. {sound_type}의 특징을 살린 편안한 내레이션
    2. 명상적이고 치유적인 내용
    3. 자연스러운 호흡 가이드 포함
    4. 마음의 평화를 찾는 내용
    5. 5-10분 분량 (약 800-1200자)
    6. 자존감 향상과 마음의 치유에 초점
    7. 시청자가 실제로 따라할 수 있는 명상 가이드
    8. 불면증, 불안, 긴장 완화에 효과적
    9. 장시간 시청용으로 알고리즘 추천에 유리
    """
    
    try:
        response = self.client.chat.completions.create(
            model=OPENAI_TEXT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        return {
            "type": "healing_sound",
            "sound_type": sound_type,
            "title": f"{sound_type}와 함께하는 힐링 시간",
            "content": content,
            "duration": "5-10분",
            "tags": ["힐링사운드", "자연음", "ASMR", "maro", "마음위로", "명상", "자존감", "수면", "불면증"],
            "structure": {
                "intro": "10초 - '오늘은 ~소리와 함께, 위로의 시간을 준비했습니다.'",
                "natural_sound": "5-10분 - 자연 사운드 루프 편집",
                "comfort_messages": "1-2분 간격으로 짧은 위로 멘트 3-4개",
                "outro": "'오늘도 수고 많았습니다. 편안한 밤 되세요.'"
            },
            "visual_elements": [
                "고정샷 영상 (창밖 비 오는 풍경, 바닷가 등)",
                "단순 패턴 애니메이션 (빗방울, 잔잔한 파도)",
                "부드러운 영상미, 따뜻한 색감"
            ],
            "audio_elements": [
                f"자연 {sound_type} 사운드 (루프 편집)",
                "1-2분 간격 위로 멘트",
                "편안한 앰비언트 BGM"
            ]
        }
    except Exception as e:
        print(f"힐링 스크립트 생성 오류: {e}")
        return self._get_fallback_healing_script(sound_type)

def _get_fallback_healing_script(self, sound_type: str) -> Dict:
    """기본 힐링 스크립트 (API 오류 시)"""
    return {
        "type": "healing_sound",
        "sound_type": sound_type,
        "title": f"{sound_type}와 함께하는 힐링 시간",
        "content": f"{sound_type} 소리를 들으며 편안하게 호흡해보세요. 모든 걱정을 내려놓고 지금 이 순간에 집중해보세요. 당신은 이미 충분히 훌륭합니다.",
        "duration": "5-10분",
        "tags": ["힐링사운드", "자연음", "ASMR", "maro", "마음위로", "명상", "자존감", "수면", "불면증"],
        "structure": {
            "intro": "10초 - '오늘은 ~소리와 함께, 위로의 시간을 준비했습니다.'",
            "natural_sound": "5-10분 - 자연 사운드 루프 편집",
            "comfort_messages": "1-2분 간격으로 짧은 위로 멘트 3-4개",
            "outro": "'오늘도 수고 많았습니다. 편안한 밤 되세요.'"
        }
    }
