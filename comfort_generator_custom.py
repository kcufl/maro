import random
from typing import Dict
from config import OPENAI_TEXT_MODEL

def generate_custom_comfort(self, situation: str = None) -> Dict:
    """맞춤형 위로 시리즈 (Target Healing) - 상황별 맞춤 위로 (3-5분)"""
    if not situation:
        situations = [
            # 감정적 상황
            "우울할 때", "불안할 때", "화가 날 때", "외로울 때",
            "스트레스 받을 때", "짜증날 때", "답답할 때", "지칠 때",
            
            # 관계적 상황
            "이별했을 때", "싸웠을 때", "오해받았을 때", "배신당했을 때",
            "외톨이일 때", "소외감을 느낄 때", "비교당할 때", "평가받을 때",
            
            # 직업적 상황
            "일이 안 될 때", "실패했을 때", "목표를 잃었을 때", "경쟁에서 밀렸을 때",
            "업무 스트레스", "번아웃", "전직 고민", "창업 실패",
            
            # 학업적 상황
            "시험 실패", "공부가 안 될 때", "목표 점수 미달성", "학업 스트레스",
            "친구들과 비교", "부모님 기대 부담", "미래에 대한 불안", "학업 포기 고민",
            
            # 건강적 상황
            "아플 때", "체중 증가", "운동 실패", "건강 습관 형성 실패",
            "수면 부족", "피로 누적", "건강 검진 결과", "만성 질환",
            
            # 재정적 상황
            "돈이 부족할 때", "빚이 많을 때", "투자 실패", "경제적 불안",
            "소비 욕구", "저축 실패", "재정 계획 실패", "경제적 독립 고민",
            
            # 일상적 상황
            "아침에 일어나기 힘들 때", "하루가 끝날 때", "주말이 끝날 때",
            "새로운 주가 시작될 때", "계절 변화", "날씨가 좋지 않을 때",
            "교통 체증", "길을 잃었을 때"
        ]
        situation = random.choice(situations)
    
    # 맞춤형 위로 전용 구조화된 프롬프트
    prompt = f"""
    {situation}에 대한 "맞춤형 위로" 콘텐츠를 작성해주세요.
    
    콘텐츠 구조:
    1. 인트로 (10초): "오늘은 {situation}에 대한 위로를 준비했습니다."
    2. 상황 공감 (1분): 해당 상황에서 느끼는 감정과 마음 상태
    3. 맞춤 위로 (2-3분): 상황에 특화된 구체적인 위로와 조언
    4. 실천 방법 (1분): 즉시 적용할 수 있는 실용적인 방법
    5. 아웃트로 (10초): "이 순간도 지나갑니다" + 다음 영상 안내
    
    요구사항:
    1. {situation}에 특화된 구체적이고 실용적인 위로
    2. 공감할 수 있는 감정 묘사와 상황 인정
    3. 즉시 적용 가능한 구체적인 방법 제시
    4. 3-5분 분량 (약 600-800자)
    5. 따뜻하고 현실적인 톤
    6. 시청자의 상황을 정확히 파악한 맞춤형 조언
    7. 자존감 향상과 실질적인 도움에 초점
    8. 상황별 맞춤형 시각 요소와 BGM 제안
    9. 감정적 공감과 실용적 해결책의 균형
    """
    
    try:
        response = self.client.chat.completions.create(
            model=OPENAI_TEXT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        
        return {
            "type": "custom_comfort",
            "situation": situation,
            "title": f"맞춤형 위로: {situation}",
            "content": content,
            "duration": "3-5분",
            "tags": ["맞춤위로", "상황별위로", "maro", "마음위로", "자존감", "실용적위로", "감정공감"],
            "structure": {
                "intro": "10초 - '오늘은 ~에 대한 위로를 준비했습니다.'",
                "empathy": "1분 - 해당 상황에서 느끼는 감정과 마음 상태",
                "custom_comfort": "2-3분 - 상황에 특화된 구체적인 위로와 조언",
                "practical_methods": "1분 - 즉시 적용할 수 있는 실용적인 방법",
                "outro": "10초 - '이 순간도 지나갑니다' + 다음 영상 안내"
            },
            "visual_elements": [
                "상황에 맞는 배경 이미지/영상",
                "감정 상태를 표현하는 색감과 모션",
                "단계별 진행을 보여주는 시각적 가이드"
            ],
            "audio_elements": [
                "상황에 맞는 BGM (우울할 때는 따뜻한, 화날 때는 차분한 등)",
                "감정 변화에 따른 음악 변화",
                "부드럽고 공감되는 내레이션"
            ]
        }
    except Exception as e:
        print(f"맞춤형 위로 생성 오류: {e}")
        return self._get_fallback_custom_comfort(situation)

def _get_fallback_custom_comfort(self, situation: str) -> Dict:
    """기본 맞춤형 위로 (API 오류 시)"""
    return {
        "type": "custom_comfort",
        "situation": situation,
        "title": f"맞춤형 위로: {situation}",
        "content": f"{situation}에 대해 이해합니다. 이런 순간은 누구에게나 찾아오는 자연스러운 일입니다. 당신의 감정을 인정하고, 작은 변화부터 시작해보세요. 모든 것은 시간이 해결해줄 것입니다.",
        "duration": "3-5분",
        "tags": ["맞춤위로", "상황별위로", "maro", "마음위로", "자존감", "실용적위로", "감정공감"],
        "structure": {
            "intro": "10초 - '오늘은 ~에 대한 위로를 준비했습니다.'",
            "empathy": "1분 - 해당 상황에서 느끼는 감정과 마음 상태",
            "custom_comfort": "2-3분 - 상황에 특화된 구체적인 위로와 조언",
            "practical_methods": "1분 - 즉시 적용할 수 있는 실용적인 방법",
            "outro": "10초 - '이 순간도 지나갑니다' + 다음 영상 안내"
        }
    }
