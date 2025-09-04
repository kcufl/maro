# maro 채널용 위로 콘텐츠 생성기 - 메인 통합 파일
# 세부 기획안에 따른 5가지 콘텐츠 타입 지원

from comfort_generator_base import ComfortContentGenerator
from comfort_generator_daily import generate_daily_comfort, _get_fallback_comfort
from comfort_generator_healing import generate_healing_sound_script, _get_fallback_healing_script
from comfort_generator_story import generate_overcome_story, _get_fallback_overcome_story
from comfort_generator_custom import generate_custom_comfort, _get_fallback_custom_comfort
from comfort_generator_challenge import generate_one_line_challenge, _get_fallback_challenge

class MaroComfortGenerator(ComfortContentGenerator):
    """maro 채널용 위로 콘텐츠 생성기 - 완전 통합 버전"""
    
    def __init__(self):
        super().__init__()
        # 각 메서드를 클래스에 바인딩
        self.generate_daily_comfort = generate_daily_comfort.__get__(self, self.__class__)
        self.generate_healing_sound_script = generate_healing_sound_script.__get__(self, self.__class__)
        self.generate_overcome_story = generate_overcome_story.__get__(self, self.__class__)
        self.generate_custom_comfort = generate_custom_comfort.__get__(self, self.__class__)
        self.generate_one_line_challenge = generate_one_line_challenge.__get__(self, self.__class__)
        
        # 폴백 메서드들도 바인딩
        self._get_fallback_comfort = _get_fallback_comfort.__get__(self, self.__class__)
        self._get_fallback_healing_script = _get_fallback_healing_script.__get__(self, self.__class__)
        self._get_fallback_overcome_story = _get_fallback_overcome_story.__get__(self, self.__class__)
        self._get_fallback_custom_comfort = _get_fallback_custom_comfort.__get__(self, self.__class__)
        self._get_fallback_challenge = _get_fallback_challenge.__get__(self, self.__class__)
    
    def generate_content_by_type(self, content_type: str, **kwargs):
        """콘텐츠 타입에 따라 적절한 생성 메서드 호출"""
        content_generators = {
            "daily_comfort": self.generate_daily_comfort,
            "healing_sound": self.generate_healing_sound_script,
            "overcome_story": self.generate_overcome_story,
            "custom_comfort": self.generate_custom_comfort,
            "one_line_challenge": self.generate_one_line_challenge
        }
        
        if content_type in content_generators:
            return content_generators[content_type](**kwargs)
        else:
            raise ValueError(f"지원하지 않는 콘텐츠 타입: {content_type}")
    
    def get_content_types_info(self):
        """지원하는 콘텐츠 타입 정보 반환 (3분 구성안 포함)"""
        return {
            "daily_comfort": {
                "name": "오늘의 위로",
                "description": "3분 습관형 루틴 콘텐츠 (인트로 15초 + 본문 2분 + 아웃로 30초)",
                "frequency": "매일",
                "purpose": "일상적인 위로와 격려",
                "structure": {
                    "timing": "0:00-0:15 인트로, 0:15-2:25 본문, 2:25-3:00 아웃로",
                    "content": "6-8개 단락으로 이어지는 위로 글귀",
                    "flow": "공감 → 감정 이해 → 위로 메시지 → 희망 제시"
                }
            },
            "healing_sound": {
                "name": "힐링 사운드 + 멘트",
                "description": "장시간 시청용 ASMR 콘텐츠 (5-10분)",
                "frequency": "주 2회 (화,토)",
                "purpose": "명상과 휴식을 위한 장시간 콘텐츠",
                "structure": {
                    "timing": "자연 사운드 루프 + 1-2분 간격 위로 멘트",
                    "content": "자연 사운드와 함께하는 명상 가이드",
                    "flow": "인트로 → 자연 사운드 → 위로 멘트 → 아웃로"
                }
            },
            "overcome_story": {
                "name": "극복 스토리 시리즈",
                "description": "단편 다큐멘터리 (5-8분)",
                "frequency": "주 1회 (수)",
                "purpose": "공감과 희망을 통한 동기부여",
                "structure": {
                    "timing": "문제 상황 → 극복 과정 → 현재 상태 → 마무리",
                    "content": "실제 경험을 바탕으로 한 극복 스토리",
                    "flow": "인트로 → 문제 → 극복 → 성장 → 희망"
                }
            },
            "custom_comfort": {
                "name": "맞춤형 위로 시리즈",
                "description": "상황별 맞춤 위로 (3-5분)",
                "frequency": "주 1회 (금)",
                "purpose": "구체적인 상황에 맞는 실용적 위로",
                "structure": {
                    "timing": "상황 공감 → 맞춤 위로 → 실천 방법 → 아웃로",
                    "content": "상황에 특화된 구체적인 위로와 조언",
                    "flow": "공감 → 위로 → 방법 → 격려"
                }
            },
            "one_line_challenge": {
                "name": "한 줄 위로 챌린지",
                "description": "커뮤니티 참여형 (3-5분)",
                "frequency": "주 1회 (일)",
                "purpose": "커뮤니티 참여와 소통",
                "structure": {
                    "timing": "챌린지 소개 → 댓글 소개 → 참여 독려 → 아웃로",
                    "content": "사용자 댓글을 통한 커뮤니티 참여",
                    "flow": "소개 → 댓글 → 참여 → 소통"
                }
            }
        }
    
    def generate_weekly_schedule(self):
        """주간 콘텐츠 계획 생성 (3분 구성안 반영)"""
        schedule = {
            "월": {
                "type": "daily_comfort", 
                "description": "새로운 한 주를 시작하는 위로 (3분)",
                "timing": "0:00-0:15 인트로, 0:15-2:25 본문, 2:25-3:00 아웃로"
            },
            "화": {
                "type": "healing_sound", 
                "description": "화요일 밤 힐링 사운드 (5-10분)",
                "timing": "자연 사운드 + 1-2분 간격 위로 멘트"
            },
            "수": {
                "type": "overcome_story", 
                "description": "중간 주 극복 스토리 (5-8분)",
                "timing": "문제 → 극복 → 성장 → 희망"
            },
            "목": {
                "type": "daily_comfort", 
                "description": "목요일 오후 위로 (3분)",
                "timing": "0:00-0:15 인트로, 0:15-2:25 본문, 2:25-3:00 아웃로"
            },
            "금": {
                "type": "custom_comfort", 
                "description": "주말을 앞둔 맞춤형 위로 (3-5분)",
                "timing": "상황 공감 → 맞춤 위로 → 실천 방법"
            },
            "토": {
                "type": "healing_sound", 
                "description": "토요일 오후 힐링 사운드 (5-10분)",
                "timing": "자연 사운드 + 1-2분 간격 위로 멘트"
            },
            "일": {
                "type": "one_line_challenge", 
                "description": "일요일 커뮤니티 챌린지 (3-5분)",
                "timing": "챌린지 소개 → 댓글 소개 → 참여 독려"
            }
        }
        return schedule
    
    def get_3min_structure_guide(self):
        """3분 위로 콘텐츠 구성 가이드 반환"""
        return {
            "title": "3분 위로 콘텐츠 세부 구성안",
            "total_duration": "3분 (180초)",
            "structure": {
                "intro": {
                    "duration": "10-15초",
                    "elements": ["채널 로고", "제목 카드", "주제 소개"],
                    "example": "오늘의 위로, 함께 나눕니다. 오늘은 '잠시 쉬어도 괜찮다'는 위로를 전합니다."
                },
                "main_content": {
                    "duration": "120-130초 (약 2분)",
                    "elements": ["이어지는 위로 글귀 낭독", "6-8개 단락", "편지/명상문 형태"],
                    "flow": ["공감", "감정 이해", "위로 메시지", "희망 제시"],
                    "timing": "한 문장 5-8초, 문장 끝마다 1-2초 멈춤"
                },
                "outro": {
                    "duration": "20-30초",
                    "elements": ["요약", "따뜻한 문구", "구독/다음 영상 안내"],
                    "example": "오늘 하루도 잘 살아내셨습니다. 내일도 함께 걸어가겠습니다."
                }
            },
            "visual_guide": {
                "background": "고정샷 (하늘, 숲길, 파도, 창밖 풍경) 또는 미니멀 애니메이션",
                "subtitle": "낭독 글귀를 그대로 자막으로 표시 (화면 중앙/하단)",
                "font": "둥근고딕, 산세리프 계열 (가독성 중심)",
                "color": "따뜻한 파스텔 톤 (노을빛, 크림색, 푸른빛)"
            },
            "audio_guide": {
                "bgm": "피아노/스트링/어쿠스틱 기타 중심, 잔잔하고 단순한 멜로디",
                "narration": "느리고 차분한 톤, 문장 끝마다 1-2초 멈춤",
                "volume": "글귀 낭독 시 낮게, 멘트 사이 공백에 살짝 올려 여운 강조"
            }
        }

# 사용 예시
if __name__ == "__main__":
    generator = MaroComfortGenerator()
    
    # 콘텐츠 타입 정보 확인
    print("=== maro 채널 콘텐츠 타입 정보 ===")
    for content_type, info in generator.get_content_types_info().items():
        print(f"{info['name']}: {info['description']}")
        if 'structure' in info:
            print(f"  구조: {info['structure']['timing']}")
    
    # 주간 스케줄 확인
    print("\n=== 주간 콘텐츠 스케줄 ===")
    for day, plan in generator.generate_weekly_schedule().items():
        print(f"{day}: {plan['description']}")
        print(f"  타이밍: {plan['timing']}")
    
    # 3분 구성 가이드 확인
    print("\n=== 3분 위로 콘텐츠 구성 가이드 ===")
    guide = generator.get_3min_structure_guide()
    print(f"제목: {guide['title']}")
    print(f"총 시간: {guide['total_duration']}")
    
    print("\nmaro 채널 콘텐츠 생성기가 준비되었습니다!")
    print("3분 위로 콘텐츠 세부 구성안이 포함되어 있습니다.")
