import random
from typing import Dict
from config import OPENAI_TEXT_MODEL

def generate_overcome_story(self, story_type: str = None) -> Dict:
    """극복 스토리 시리즈 (Overcome Stories) - 단편 다큐멘터리 (5-8분)"""
    if not story_type:
        story_types = [
            # 개인적 어려움 극복
            "우울증 극복", "불안장애 극복", "자살생각 극복", "트라우마 극복",
            "중독 극복", "식사장애 극복", "수면장애 극복", "공포증 극복",
            
            # 관계적 어려움 극복
            "이별 극복", "이혼 극복", "가족갈등 극복", "친구관계 극복",
            "직장갈등 극복", "왕따 극복", "배신 극복", "외로움 극복",
            
            # 직업적 어려움 극복
            "실직 극복", "전직 극복", "업무 스트레스 극복", "번아웃 극복",
            "목표 달성 실패 극복", "경력 전환 극복", "창업 실패 극복", "시험 실패 극복",
            
            # 건강적 어려움 극복
            "질병 극복", "사고 후 회복", "만성질환 극복", "체중 관리 극복",
            "운동 습관 형성", "금연 극복", "금주 극복", "건강한 식습관 형성",
            
            # 재정적 어려움 극복
            "빚 갚기", "파산 극복", "투자 실패 극복", "사기 피해 극복",
            "경제적 독립", "저축 습관 형성", "재정 계획 수립", "소비 습관 개선"
        ]
        story_type = random.choice(story_types)
    
    # 극복 스토리 전용 구조화된 프롬프트
    prompt = f"""
    {story_type}를 극복한 사람의 이야기를 "극복 스토리" 형식으로 작성해주세요.
    
    콘텐츠 구조:
    1. 인트로 (15초): "오늘의 극복 스토리: {story_type}" + 짧은 BGM
    2. 문제 상황 (1-2분): 구체적인 어려움과 감정 상태
    3. 극복 과정 (2-3분): 단계별 극복 방법과 노력
    4. 현재 상태 (1분): 극복 후의 변화와 성장
    5. 마무리 메시지 (30초): 시청자에게 전하는 희망의 메시지
    6. 아웃트로 (10초): "당신도 충분히 할 수 있습니다" + 다음 영상 안내
    
    요구사항:
    1. 실제 경험을 바탕으로 한 현실적인 스토리
    2. 공감할 수 있는 감정과 상황 묘사
    3. 구체적이고 실용적인 극복 방법 제시
    4. 5-8분 분량 (약 1000-1500자)
    5. 희망적이지만 과장되지 않은 톤
    6. 시청자가 자신의 상황에 적용할 수 있는 인사이트
    7. 자존감 향상과 용기 부여에 초점
    8. 인터뷰 톤의 내레이션으로 구성
    9. 점진적인 BGM 변화로 감정 고조
    """
    
    try:
        response = self.client.chat.completions.create(
            model=OPENAI_TEXT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        return {
            "type": "overcome_story",
            "story_type": story_type,
            "title": f"극복 스토리: {story_type}",
            "content": content,
            "duration": "5-8분",
            "tags": ["극복스토리", "동기부여", "희망", "maro", "마음위로", "자존감", "성장", "극복"],
            "structure": {
                "intro": "15초 - '오늘의 극복 스토리: ~' + 짧은 BGM",
                "problem": "1-2분 - 구체적인 어려움과 감정 상태",
                "overcoming": "2-3분 - 단계별 극복 방법과 노력",
                "current_state": "1분 - 극복 후의 변화와 성장",
                "closing": "30초 - 시청자에게 전하는 희망의 메시지",
                "outro": "10초 - '당신도 충분히 할 수 있습니다' + 다음 영상 안내"
            },
            "visual_elements": [
                "사진/영상 자료 (블러 처리, 개인정보 보호)",
                "단계별 진행을 보여주는 애니메이션",
                "감정 변화를 표현하는 색감 변화"
            ],
            "audio_elements": [
                "점진적으로 고조되는 BGM",
                "인터뷰 톤의 내레이션",
                "감정적 순간의 사운드 이펙트"
            ]
        }
    except Exception as e:
        print(f"극복 스토리 생성 오류: {e}")
        return self._get_fallback_overcome_story(story_type)

def _get_fallback_overcome_story(self, story_type: str) -> Dict:
    """기본 극복 스토리 (API 오류 시)"""
    return {
        "type": "overcome_story",
        "story_type": story_type,
        "title": f"극복 스토리: {story_type}",
        "content": f"{story_type}를 극복한 한 사람의 이야기입니다. 처음에는 모든 것이 어려워 보였지만, 작은 변화부터 시작해서 결국 극복할 수 있었습니다. 당신도 충분히 할 수 있습니다.",
        "duration": "5-8분",
        "tags": ["극복스토리", "동기부여", "희망", "maro", "마음위로", "자존감", "성장", "극복"],
        "structure": {
            "intro": "15초 - '오늘의 극복 스토리: ~' + 짧은 BGM",
            "problem": "1-2분 - 구체적인 어려움과 감정 상태",
            "overcoming": "2-3분 - 단계별 극복 방법과 노력",
            "current_state": "1분 - 극복 후의 변화와 성장",
            "closing": "30초 - 시청자에게 전하는 희망의 메시지",
            "outro": "10초 - '당신도 충분히 할 수 있습니다' + 다음 영상 안내"
        }
    }
